import os

from charmy.constants import LINUX_INSTALLATION_ICON, LINUX_INSTALLATION_EXEC

from ..installer import BaseLinuxInstaller
from . import UID
from .constants import LAUNCHER_CONTENT_PATTERN

class UbuntuInstaller(BaseLinuxInstaller):
    """
    Ubuntu specific installer.
    """
    os = UID

    def install(self, file, destination=None):
        """

        :param file:
        :return:
        """
        # First do as parent does
        installed = super(UbuntuInstaller, self).install(file, destination)

        # If installation directory does not yet exist, create it.
        installation_dir = destination or self.installation_dir
        latest_installation_dir = os.path.join(installation_dir,
                                               self.latest_installation_dir)

        launcher_path = os.path.join(
            os.path.expanduser('~'),
            '.local/share/applications/jetbrains-pycharm-ce.desktop'
        )
        icon_path = os.path.join(latest_installation_dir,
                                 LINUX_INSTALLATION_ICON)
        exec_path = os.path.join(latest_installation_dir,
                                 LINUX_INSTALLATION_EXEC)
        launcher_content = LAUNCHER_CONTENT_PATTERN.format(
            **{
                'icon_path': icon_path,
                'exec_path': exec_path,
            }
        )

        #if not os.path.isfile(launcher_path):
        # Create a launcher
        launcher_file =open(launcher_path, 'w+')
        launcher_file.write(launcher_content)
        launcher_file.close()

        return installed
