__title__ = 'charmy.utils'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('get_installer',)

import platform

from .constants import PLATFORM_LINUX
from .installers.linux.ubuntu import UID as LINUX_UBUNTU_UID
from .installers.linux.ubuntu.installer import UbuntuInstaller
from .installers.linux.other.installer import OtherLinuxInstaller

def get_installer():
    """

    :return:
    """
    current_platform = platform.uname()

    if current_platform[0] == PLATFORM_LINUX:
        dist = platform.dist()
        if dist[0] == LINUX_UBUNTU_UID:
            return UbuntuInstaller()
        else:
            return OtherLinuxInstaller()
