import os
import shutil
import tarfile

from charmy.base import BaseInstaller
from charmy.constants import (
    PLATFORM_LINUX, LINUX_EXTENSION, LINUX_INSTALLATION_DIR, LINUX_TEMP_DIR,
    LATEST_INSTALLATION_DIR, LINUX_LATEST_INSTALLATION_EXEC, LINUX_CONFIG_DIR,
    LINUX_INSTALLATION_EXEC
)

class BaseLinuxInstaller(BaseInstaller):
    """
    """
    platform = PLATFORM_LINUX
    installation_dir = LINUX_INSTALLATION_DIR
    config_dir = LINUX_CONFIG_DIR
    temp_dir = LINUX_TEMP_DIR
    latest_installation_dir = LATEST_INSTALLATION_DIR
    latest_installation_exec = LINUX_LATEST_INSTALLATION_EXEC

    def setup(self, file, destination=None):
        """

        :param file:
        :return:
        """
        # If installation directory does not yet exist, create it.
        installation_dir = destination or self.installation_dir
        if not os.path.exists(installation_dir):
            os.makedirs(installation_dir)

        # Full path to the filename once it would be in the `installation_dir`.
        new_file = os.path.join(installation_dir, os.path.basename(file))

        # If downloaded file is not yet in the installation directory, copy it.
        if not os.path.isfile(new_file):
            shutil.copy(file, installation_dir)

        # Unpack the archive.
        archive = tarfile.open(new_file)
        archive.extractall(installation_dir)
        archive.close()

        # This is the new of directory to which the files were extracted.
        distribution_dir = new_file.replace('.{0}'.format(LINUX_EXTENSION), '')

        latest_installation_dir = os.path.join(installation_dir,
                                               self.latest_installation_dir)

        # First removing old symlinks.
        if os.path.exists(latest_installation_dir):
            os.remove(latest_installation_dir)

        # Symlink directory.
        os.symlink(distribution_dir, latest_installation_dir)

        exec_file = os.path.join(
            self.latest_installation_dir,
            LINUX_INSTALLATION_EXEC
        )
        latest_installation_exec = os.path.join(installation_dir,
                                                self.latest_installation_exec)

        # First removing old symlinks.
        if os.path.isfile(latest_installation_exec):
            os.remove(latest_installation_exec)

        # Symlink executable.
        os.symlink(exec_file, latest_installation_exec)

        return True

    def activate(self, version, edition):
        """

        :return:
        """
        destination = self._read_destination_from_config_ini()

        installation_dir = destination or self.installation_dir
        latest_installation_dir = os.path.join(installation_dir,
                                               self.latest_installation_dir)
        # First removing old symlinks.
        if os.path.exists(latest_installation_dir):
            os.remove(latest_installation_dir)

        distribution_dir = os.path.join(
            installation_dir,
            "pycharm-{0}-{1}".format(edition, version)
        )
        # Symlink directory.
        os.symlink(distribution_dir, latest_installation_dir)

        exec_file = os.path.join(
            self.latest_installation_dir,
            LINUX_INSTALLATION_EXEC
        )
        latest_installation_exec = os.path.join(installation_dir,
                                                self.latest_installation_exec)

        # First removing old symlinks.
        if os.path.isfile(latest_installation_exec):
            os.remove(latest_installation_exec)

        # Symlink executable.
        os.symlink(exec_file, latest_installation_exec)

        return (True, installation_dir, '')
