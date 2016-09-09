from ..installer import BaseLinuxInstaller
from . import UID

__title__ = 'charmy.installers.linux.other'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('OtherLinuxInstaller',)


class OtherLinuxInstaller(BaseLinuxInstaller):
    """Other Linux installer."""

    os = UID
