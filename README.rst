======
charmy
======
An automated PyCharm installer.

Supported systems
=================
At the moment works for Linux only.

Although `charmy` would work on any Linux system (download, sym-link), some
extra things, like creating a `.desktop` file for Ubuntu launcher, are done for
specific systems only.

Installation
============
Install with latest stable version from PyPI::

    $ pip install charmy

Or install the latest stable version from GitHub::

    $ pip install -e git+https://github.com/barseghyanartur/charmy@stable#egg=charmy

Or install the latest stable version from BitBucket::

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/charmy@stable#egg=charmy

Or install into python path::

    $ python setup.py install

That's all. See the `Usage and examples` section for more.

Usage and examples
==================
Basics
------
Install latest version of the PyCharm. Let's assume the you want
to install community edition version 4.5.4::

    charmy install --version=4.5.4 --edition=community

List installed PyCharm versions::

    charmy versions

Switch between installed PyCharm versions (imagine, you have both 4.5.3
and 4.5.4 installed and want to switch back to previous version)::

    charmy activate --version=4.5.3 --edition=community

If you don't have a version preference and just want to install the latest 
version available (defaults to community edition), just type::

    charmy install

You may be more explicit as well::

    charmy install --edition=community

Install the latest professional version::

    charmy install --edition=professional

By default `charmy` installs PyCharm in the `PyCharm` directory. If you want it
to be installed elsewhere provide --destination directive::

    charmy install --destination=/home/user/pycharm/

Note, that `charmy` remembers your last destination, so once you have
specified a destination, you don't have to specify it again (unless you
want to change installation directory).

Ubuntu
------
When installing on Ubuntu, `charmy` creates a `.desktop` file for to be drag
and dropped to the Unity launcher. The `.desktop` file is located at::

    ~/.local/share/applications/jetbrains-pycharm-ce.desktop

License
=======
GPL 2.0/LGPL 2.1

Support
=======
For any issues contact me at the e-mail given in the `Author` section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
