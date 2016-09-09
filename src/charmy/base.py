import os

from six.moves import configparser

from sqlalchemy.exc import IntegrityError

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from .constants import (
    EDITIONS, PLATFORMS, DOWNLOAD_LINK_PATTERN, PLATFORM_EXTENSIONS, DB_NAME,
    CONFIG_INI_FILE_NAME, CONFIG_SECTION_PATHS, CONFIG_OPTION_DESTINATION
)
from .helpers import download_file

__title__ = 'charmy.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseInstaller',)


class BaseInstaller(object):
    """Base installer.

        - uid (str): Unique identifier of the installer.
        - platform (str): Platform.
        - installation_dir (str): Absolute path to directory in which the
                                  PyCharm would be installed.
        - config_dir (str): Absolute path to directory in which the
                            Charmy configuration files and the database would
                            be stored.
        - temp_dir (str): Absolute path to temp directory in which the
                          PyCharm distributions would be downloaded.
        - latest_installation_dir (str): Relative path (from `installation_dir`)
                                         to directory which the specific
                                         PyCharm installation would be
                                         sym-linked to.
        - latest_installation_exec (str): Relative path (from
                                         `installation_dir`) to executable
                                         which would sym-link to latest
                                         PyCharm executable.
        - db_ready (bool): Indicates whether database is ready.
    """

    os = None
    platform = None
    installation_dir = None
    config_dir = None
    temp_dir = None
    latest_installation_dir = None
    latest_installation_exec = None

    db_ready = False # Indicates whether database is ready

    def __init__(self, *args, **kwargs):
        """Constructor.

        :param args:
        :param kwargs:
        :return:
        """
        assert self.platform and self.platform in PLATFORMS
        assert self.os
        assert self.installation_dir
        assert self.config_dir
        assert self.temp_dir
        assert self.latest_installation_dir
        assert self.latest_installation_exec

        self._create_dirs()

        self.extension = PLATFORM_EXTENSIONS.get(self.platform)
        self.db_name = os.path.join(self.config_dir, DB_NAME)
        self.config_ini_filename = os.path.join(self.config_dir,
                                                CONFIG_INI_FILE_NAME)
        self._create_files()
        self._sync_db()

    def _create_dirs(self):
        """Create dirs (internal method)."""
        dirs = (
            self.installation_dir,
            self.config_dir,
            self.temp_dir,
        )
        for dir_path in dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        return True

    def _create_files(self):
        """Create files (internal method)."""
        if not os.path.isfile(self.config_ini_filename):
            config_ini_file = open(self.config_ini_filename, 'w')
            config_ini_file.close()

    def _prepare_db(self):
        """Prepare the database (create if not exist).

        Also, prepare the models.

        :return:
        """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(
            self.db_name
        )
        self.db = SQLAlchemy(self.app)
        self.distribution_cls = self._get_distribution_class()
        self.db_ready = True

    def drop_db(self):
        """Drop the database.

        :return:
        """
        if os.path.isfile(self.db_name):
            os.remove(self.db_name)

    def _get_distribution_class(self):
        """Get the `Distribution` model for saving installed distributions.

        :return:
        """
        db = self.db

        class Distribution(db.Model):
            """Distribution model for saving installed distributions."""

            id = db.Column(db.Integer, primary_key=True)
            version = db.Column(db.String(80))
            edition = db.Column(db.String(120))
            path = db.Column(db.String(120))
            active = db.Column(db.Boolean())

            __table_args__ = (
                db.UniqueConstraint(
                    'version',
                    'edition',
                    'path',
                    name='version_edition_path_unique'
                ),
            )

            def __init__(self, version, edition, path, active):
                """Constructor."""
                self.version = version
                self.edition = edition
                self.path = path
                self.active = active

            def __repr__(self):
                """Representation."""
                return '<Distribution {0} {1}>'.format(self.version,
                                                       self.edition,
                                                       self.path,
                                                       self.active)

        return Distribution

    def _sync_db(self):
        """Create database if not exist.

        :return:
        """
        if not self.db_ready:
            self._prepare_db()
        self.db.create_all()

    def download(self, version, edition, use_cache=True):
        """Download the PyCharm.

        :param version:
        :param edition:
        :param bool use_cache:
        :return:
        """
        assert edition in EDITIONS
        download_link = self._build_download_link(version, edition)
        downloaded_file = download_file(download_link, self.temp_dir,
                                        use_cache=use_cache)
        return downloaded_file

    def _build_download_link(self, version, edition):
        """Build download link."""
        return DOWNLOAD_LINK_PATTERN.format(
            **{
                'edition': edition,
                'version': version,
                'extension': self.extension
             }
        )

    def _install(self, version, edition, use_cache=True, destination=None):
        """Install the downloaded PyCharm file (internal method).

        :param str version:
        :param str edition:
        :param bool use_cache:
        :param str destination:
        :return tuple: (success, destination, message)
        """
        if destination:
            self._write_destination_info_to_config_ini(destination)
        else:
            destination = self._read_destination_from_config_ini()

        downloaded_file = self.download(version, edition, use_cache=use_cache)
        installed = self.install(downloaded_file, destination)

        installation_dir = destination or self.installation_dir

        if installed:
            self._write_distribution_info_to_db(version,
                                                edition,
                                                installation_dir)
            return (True, installation_dir, '')
        else:
            return (False, installation_dir, '')

    def install(self, file, destination=None):
        """Install the downloaded PyCharm.

        This method should return True on success. Otherwise considered to
        be failed.

        :param file:
        :return bool:
        """
        raise NotImplemented

    def _write_destination_info_to_config_ini(self, destination):
        """Write destination info to the config.ini.

        :param str destination:
        :return:
        """
        config_ini_file = open(self.config_ini_filename, 'w+')
        Config = configparser.ConfigParser()
        Config.add_section(CONFIG_SECTION_PATHS)
        Config.set(CONFIG_SECTION_PATHS, CONFIG_OPTION_DESTINATION, destination)
        Config.write(config_ini_file)
        config_ini_file.close()

    def _read_destination_from_config_ini(self):
        """Read destination from config ini.

        :return str:
        """
        destination = None
        config_ini_file = open(self.config_ini_filename)
        Config = configparser.ConfigParser()
        Config.readfp(config_ini_file)
        try:
            destination = Config.get(CONFIG_SECTION_PATHS,
                                     CONFIG_OPTION_DESTINATION)
        except Exception as err:
            pass

        config_ini_file.close()

        return destination

    def _write_distribution_info_to_db(self, version, edition,
                                       installation_dir):
        """Write distribution data into the database.

        Return True on success and False on duplicates.

        :param str version:
        :param str edition:
        :return bool:
        """
        # First of all, since we're about to set the distribution as default,
        # we need to mark existing one as non-active.
        self.distribution_cls \
            .query \
            .filter_by(path=installation_dir, active=True) \
            .update({"active": False})
        self.db.session.commit()

        # Now save the distribution.
        distribution = self.distribution_cls(version,
                                             edition,
                                             installation_dir,
                                             True)
        try:
            self.db.session.add(distribution)
            self.db.session.commit()
            return True
        except IntegrityError as err:
            self.db.session.rollback()
            self.distribution_cls \
                .query \
                .filter_by(version=version,
                           edition=edition,
                           path=installation_dir) \
                .update({"active": True})
            self.db.session.commit()

            return False

    def _versions(self):
        """List installed versions (internal method).

        :return:
        """
        return ["{0}        {1}        {2}        {3}".format(dist.version,
                                         dist.edition,
                                         dist.path,
                                         "(active)" if dist.active else "")
                for dist in self.distribution_cls.query.all()]

    def versions(self):
        """List installed versions."""
        return self._versions()

    def _uninstall(self, version, edition):
        """Uninstall given version/edition (internal method).

        :param version:
        :param edition:
        :return:
        """
        return self.uninstall(version, edition)

    def uninstall(self, version, edition):
        """Uninstall given version/edition."""
        raise NotImplemented

    def _activate(self, version, edition):
        """Activate given version/edition (internal method)."""
        activated, installation_dir, message = self.activate(version, edition)
        if activated:
            self._write_distribution_info_to_db(version,
                                                edition,
                                                installation_dir)
        return (activated, installation_dir, message)

    def activate(self, version, edition):
        """Activate given version/edition.

        This method should return a tuple (True, destination, message) on
        success. Otherwise considered to be failed.

        :param version:
        :param edition:
        :return:
        """
        raise NotImplemented
