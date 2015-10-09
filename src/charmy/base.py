__title__ = 'charmy.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseInstaller',)

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

class BaseInstaller(object):
    """
    Base installer.

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
        """

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
        if not os.path.isfile(self.config_ini_filename):
            config_ini_file = open(self.config_ini_filename, 'w')
            config_ini_file.close()

    def _prepare_db(self):
        """
        Prepare the database (create if not exist). Prepare the models.

        :return:
        """
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{0}'.format(
            self.db_name
        )
        self.db = SQLAlchemy(self.app)
        self.distribution_cls = self._get_distribution_class()
        self.db_ready = True

    def _get_distribution_class(self):
        """
        Gets the `Distribution` model for saving installed distributions.

        :return:
        """
        db = self.db

        class Distribution(db.Model):
            """
            Distribution model for saving installed distributions.
            """
            id = db.Column(db.Integer, primary_key=True)
            version = db.Column(db.String(80))
            edition = db.Column(db.String(120))

            __table_args__ = (
                db.UniqueConstraint(
                    'version',
                    'edition',
                    name='version_edition_unique'
                ),
            )

            def __init__(self, version, edition):
                self.version = version
                self.edition = edition

            def __repr__(self):
                return '<Distribution {0} {1}>'.format(self.version,
                                                       self.edition)

        return Distribution

    def _sync_db(self):
        """
        Creates database if not exist.
        :return:
        """
        if not self.db_ready:
            self._prepare_db()
        self.db.create_all()

    def download(self, version, edition, use_cache=True):
        """
        Downloads the PyCharm
        :param version:
        :param edition:
        :return:
        """
        assert edition in EDITIONS
        download_link = self._build_download_link(version, edition)
        downloaded_file = download_file(download_link, self.temp_dir,
                                        use_cache=use_cache)
        return downloaded_file

    def _build_download_link(self, version, edition):
        return DOWNLOAD_LINK_PATTERN.format(
            **{
                'edition': edition,
                'version': version,
                'extension': self.extension
             }
        )

    def install(self, version, edition, use_cache=True, destination=None):
        """
        Installs the downloaded PyCharm file.

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
        installed = self.setup(downloaded_file, destination)

        if installed:
            self._write_distribution_info_to_db(version, edition)
            return (True, destination, '')
        else:
            return (False, destination, '')

    def _write_destination_info_to_config_ini(self, destination):
        """

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
        """
        Reads destination from config ini.

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

    def _write_distribution_info_to_db(self, version, edition):
        """
        Writes distribution data into the database. Returns True on success
        and False on duplicates.

        :param str version:
        :param str edition:
        :return bool:
        """
        # Save distribution.
        distribution = self.distribution_cls(version, edition)
        self.db.session.add(distribution)
        try:
            self.db.session.commit()
            return True
        except IntegrityError as err:
            return False

    def versions(self):
        """
        Gets installed versions.

        :return:
        """
        return ["{0} {1}".format(dist.version, dist.edition)
                for dist in self.distribution_cls.query.all()]

    def uninstall(self, version, edition):
        """

        :param version:
        :param edition:
        :return:
        """
        raise NotImplemented

    def setup(self, file, destination=None):
        """
        This method should return True on success. Otherwise considered to
        be failed.

        :param file:
        :return bool:
        """
        raise NotImplemented

    def activate(self, version, edition):
        """
        This method should return a tuple (True, destination, message) on
        success. Otherwise considered to be failed.

        :param version:
        :param edition:
        :return:
        """
        raise NotImplemented
