__title__ = 'charmy.constants'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BASE_DIR', 'LINUX_EXTENSION', 'PLATFORM_LINUX', 'PLATFORM_EXTENSIONS',
    'EDITION_PROFESSIONAL', 'EDITION_COMMUNITY', 'EDITIONS', 'DEFAULT_EDITION',
    'DOWNLOAD_LINK_PATTERN', 'DOWNLOAD_PAGE_LINK', 'VERSION_JS_URL',
    'ACTION_INSTALL', 'ACTION_UNINSTALL', 'ACTION_ACTIVATE', 'ACTION_VERSIONS',
    'ACTION_CHECK_LATEST_AVAILABLE', 'ACTIONS', 'DOWNLOAD_CACHE_DIR',
    'LATEST_INSTALLATION_DIR', 'DB_NAME', 'CONFIG_INI_FILE_NAME',
    'LINUX_LATEST_INSTALLATION_EXEC', 'LINUX_TEMP_DIR', 'LINUX_CONFIG_DIR',
    'LINUX_INSTALLATION_EXEC', 'LINUX_INSTALLATION_ICON',
    'CONFIG_SECTION_PATHS', 'CONFIG_OPTION_DESTINATION',
)

import os

def not_implemented():
    """
    For raising not implemented errors on constants.
    :return:
    """
    raise NotImplemented

NOT_IMPLEMENTED_LAMBDA = lambda: not_implemented()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# ***************************************************************************
# ***************************** File extensions *****************************
# ***************************************************************************
LINUX_EXTENSION = 'tar.gz'
MACOSX_EXTENSION = 'dmg'
WINDOWS_EXTENSION = 'exe'

# ***************************************************************************
# ******************************* Platforms *********************************
# ***************************************************************************
PLATFORM_LINUX = 'Linux'
PLATFORM_MACOSX = 'Mac OS X'
PLATFORM_WINDOWS = 'Windows'
PLATFORMS = (PLATFORM_LINUX, PLATFORM_MACOSX, PLATFORM_WINDOWS)
DEFAULT_PLATFORM = PLATFORM_LINUX

# Platform <-> File extension mapping
PLATFORM_EXTENSIONS = {
    PLATFORM_LINUX: LINUX_EXTENSION,
    PLATFORM_MACOSX: MACOSX_EXTENSION,
    PLATFORM_WINDOWS: WINDOWS_EXTENSION
}

# ***************************************************************************
# ******************************** Editions *********************************
# ***************************************************************************
EDITION_PROFESSIONAL = 'professional'
EDITION_COMMUNITY = 'community'
EDITIONS = (EDITION_PROFESSIONAL, EDITION_COMMUNITY)
DEFAULT_EDITION = EDITION_COMMUNITY

# ***************************************************************************
# ***************************** Download links ******************************
# ***************************************************************************
DOWNLOAD_LINK_PATTERN = "http://download-cf.jetbrains.com/python/pycharm-" \
                        "{edition}-{version}.{extension}"
DOWNLOAD_PAGE_LINK = 'https://www.jetbrains.com/pycharm/download/index.html'
VERSION_JS_URL = 'https://www.jetbrains.com/js2/version.js'

# ***************************************************************************
# ******************************** Actions **********************************
# ***************************************************************************
ACTION_INSTALL = 'install'
ACTION_UNINSTALL = 'unistall'
ACTION_ACTIVATE = 'activate'
ACTION_VERSIONS = 'versions'
ACTION_CHECK_LATEST_AVAILABLE = 'check-latest-available'
ACTIONS = (
    ACTION_INSTALL,
    ACTION_ACTIVATE,
    ACTION_UNINSTALL,
    ACTION_VERSIONS,
    ACTION_CHECK_LATEST_AVAILABLE
)

# ***************************************************************************
# *************************** Config options ********************************
# ***************************************************************************
CONFIG_SECTION_PATHS = 'paths'
CONFIG_OPTION_DESTINATION = 'destination'

# ***************************************************************************
# ****************************** Directories ********************************
# ***************************************************************************
# Download cache, relative path from the charmy directory.
DOWNLOAD_CACHE_DIR = 'download_cache'

# Latest installation directory, relative path from the installation directory.
# This would be used as a name of the sym-link.
LATEST_INSTALLATION_DIR = 'pycharm-latest'

DB_NAME = 'charmy.sqlite'

CONFIG_INI_FILE_NAME = 'config.ini'

# Latest executable, relative filename. This would be used as a name of the
# sym-link.
LINUX_LATEST_INSTALLATION_EXEC = 'pycharm-latest.sh'
MACOSX_LATEST_INSTALLATION_EXEC = NOT_IMPLEMENTED_LAMBDA # TODO
WINDOWS_LATEST_INSTALLATION_EXEC = NOT_IMPLEMENTED_LAMBDA # TODO

# Installation directory. Absolute path to.
LINUX_INSTALLATION_DIR = os.path.join(os.path.expanduser('~'), 'PyCharm')
MACOSX_INSTALLATION_DIR = NOT_IMPLEMENTED_LAMBDA # TODO
WINDOWS_INSTALLATION_DIR = NOT_IMPLEMENTED_LAMBDA # TODO

# Temp directory. Absolute path to.
LINUX_TEMP_DIR = '/var/tmp/charmy/'
MACOSX_TEMP_DIR = NOT_IMPLEMENTED_LAMBDA # TODO
WINDOWS_TEMP_DIR = NOT_IMPLEMENTED_LAMBDA # TODO

# Config directory. Absolute path to. In this directory Charmy
# configuration files would be stored, such as database.
LINUX_CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.charmy')
MACOSX_CONFIG_DIR = NOT_IMPLEMENTED_LAMBDA # TODO
WINDOWS_CONFIG_DIR = NOT_IMPLEMENTED_LAMBDA # TODO

# Path to actual PyCharm executable, relative from the directory it's
# extracted to.
LINUX_INSTALLATION_EXEC = 'bin/pycharm.sh'
MACOSX_INSTALLATION_EXEC = NOT_IMPLEMENTED_LAMBDA # TODO
WINDOWS_INSTALLATION_EXEC = NOT_IMPLEMENTED_LAMBDA # TODO

# Path to actual PyCharm icon, relative from the directory it's
# extracted to.
LINUX_INSTALLATION_ICON = 'bin/pycharm.png'
MACOSX_INSTALLATION_ICON = NOT_IMPLEMENTED_LAMBDA # TODO
WINDOWS_INSTALLATION_ICON = NOT_IMPLEMENTED_LAMBDA # TODO
