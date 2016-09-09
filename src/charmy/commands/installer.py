from __future__ import print_function

__title__ = 'charmy.commands.installer'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('main',)

import argparse

from ..constants import (
    DEFAULT_EDITION, ACTIONS, ACTION_INSTALL, ACTION_ACTIVATE, ACTION_VERSIONS,
    ACTION_UNINSTALL, ACTION_CHECK_LATEST_AVAILABLE, ACTION_RESET_SETTINGS,
    ACTION_DISCOVER_INSTALLED_VERSIONS
)
from ..utils import get_installer
from ..helpers import detect_latest_version

def _install(installer, **kwargs):
    print("  Installing PyCharm version {0} ({1} edition)"
              "".format(kwargs.get('version', None),
                        kwargs.get('edition', None)))
    res = installer._install(**kwargs)
    if res[0]:
        print("  Successfully installed to {0}".format(res[1]))
    else:
        print("  Installation failed!")

def _activate(installer, **kwargs):
    print("  Activating PyCharm version {0} ({1} edition)"
          "".format(kwargs.get('version', None),
                    kwargs.get('edition', None)))
    res = installer._activate(**kwargs)
    if res[0]:
        print("  Successfully activated in {0}".format(res[1]))
    else:
        print("  Activation failed!")

def _versions(installer, **kwargs):
    print("  Listing installed PyCharm versions (version, edition)")
    res = installer.versions(**kwargs)
    for r in res:
        print("  - {0}".format(r))

def _uninstall(installer, **kwargs):
    res = installer._uninstall(**kwargs)
    #print(res)

def _check_latest_available(latest_version):
    res = latest_version or detect_latest_version()
    if res:
        print("  {0}".format(res))
    else:
        print("  Could not fetch information on latest version "
              "available ")

def _discover_installed_versions(installer, **kwargs):
    res = installer.discover_installed_versions(**kwargs)
    if res:
        print("  {0}".format(res))
    else:
        print("  Could not fetch information on latest version "
              "available ")

def main():
    """
    PyCharm installer.

    :return:
    """
    parser = argparse.ArgumentParser(description="""
    PyCharm installer.
    """)
    parser.add_argument("action", metavar="ACTION", type=str,
                        help="`action` value", )
    parser.add_argument("-v", "--version", dest="version", type=str,
                        help="`version` value", metavar="VERSION")
    parser.add_argument("-e", "--edition", dest="edition", type=str,
                        help="`edition` value", metavar="EDITION")
    parser.add_argument("-n", "--usecache", dest="usecache", type=str,
                        help="`usecache` value", metavar="USECACHE")
    parser.add_argument("-d", "--destination", dest="destination", type=str,
                        help="`destination` value", metavar="DESTINATION")
    args = parser.parse_args()

    kwargs_install = {}
    kwargs_activate = {}
    kwargs_versions = {}
    kwargs_uninstall = {}
    kwargs_discover_installed_versions = {}

    latest_version = None
    if args.version:
        kwargs_install.update({'version': args.version})
        kwargs_activate.update({'version': args.version})
    else:
        if args.action == ACTION_INSTALL:
            latest_version = detect_latest_version()
            if latest_version:
                kwargs_install.update({'version': latest_version})
                kwargs_activate.update({'version': latest_version})

    try:
        edition = args.edition
    except:
        edition = None

    if not edition:
        edition = DEFAULT_EDITION

    kwargs_install.update({'edition': edition})
    kwargs_activate.update({'edition': edition})

    try:
        use_cache = False if args.nocache == 'no' else True
    except:
        use_cache = True

    kwargs_install.update({'use_cache': use_cache})

    if args.destination:
        kwargs_install.update({'destination': args.destination})
        kwargs_discover_installed_versions.update(
            {'destination': args.destination}
        )
    try:
        installer = get_installer()
    except Exception as err:
        raise err

    if installer:
        res = None
        if args.action == ACTION_INSTALL:
            _install(installer, **kwargs_install)

        elif args.action == ACTION_ACTIVATE:
            _activate(installer, **kwargs_activate)

        elif args.action == ACTION_VERSIONS:
            _versions(installer, **kwargs_versions)

        elif args.action == ACTION_UNINSTALL:
            _uninstall(installer, **kwargs_uninstall)

        elif args.action == ACTION_CHECK_LATEST_AVAILABLE:
            _check_latest_available(latest_version)

        elif args.action == ACTION_DISCOVER_INSTALLED_VERSIONS:
            _discover_installed_versions(installer,
                                        **kwargs_discover_installed_versions)

        elif args.action == ACTION_RESET_SETTINGS:
            installer._reset_settings()


if __name__ == "__main__":
    main()
