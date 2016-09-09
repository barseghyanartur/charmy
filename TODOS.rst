=============
TODOS/Roadmap
=============

TODOS
=====
Base on MoSCoW principle. Must haves and should haves are planned to be worked
on.

* Features/issues marked with plus (+) are implemented/solved.
* Features/issues marked with minus (-) are yet to be implemented.

Must haves
----------
+ When installing from PyPI and then charmy install, gives the following
  error message:
  """
  /path/to/env/charmy-env/bin/python: bad interpreter:
  No such file or directory
  """
+ When having installed with default settings (no --destination provided),
  the following message is shown:
  "Successfully installed to None"
+ When having installed with default settings (no --destination provided)
  and then activate another, the following message is shown:
  "Successfully activated in None"
+ Make a command to fetch the latest version available: charmy latest
+ In the versions command output, make clear which version is currently active.
+ Add notes on installing in virtualenv (since that's the recommended way to
  install) and making sure that there are no running PyCharm instances, when
  installing new versions.
- Installing professional version doesn't work. If you try to do so, activating
  the community version doesn't work either.
- Make a `discover-installed-versions` command to discover locally installed
  PyCharm versions and make appropriate database updates.

Should haves
------------
- Add icon creation and shortcut for Ubuntu installer.
- Fedora installer.
- RedHat installer.

Could haves
-----------

Would haves
-----------
- Mac OS X installer.
- Windows installer.
