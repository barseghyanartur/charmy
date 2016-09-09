======
charmy
======
An automated PyCharm installer for Linux.

Supported systems
=================
Although `charmy` would work on any Linux system (download, sym-link), some
extra things, like creating a `.desktop` file for Ubuntu launcher, are done for
specific systems only.

Installation
============
Install with latest stable version from PyPI:

.. code-block:: sh

    pip install charmy

Or install the latest stable version from GitHub:

.. code-block:: sh

    pip install -e git+https://github.com/barseghyanartur/charmy@stable#egg=charmy

Or install the latest stable version from BitBucket:

.. code-block:: sh

    pip install -e hg+https://bitbucket.org/barseghyanartur/charmy@stable#egg=charmy

Or install into python path:

.. code-block:: sh

    $ python setup.py install

That's all. See the `Usage and examples` section for more.

Usage and examples
==================
Basics
------
Install the latest version of PyCharm (defaults to community edition):

.. code-block:: sh

    charmy install

You may be more explicit as well:

.. code-block:: sh

    charmy install --edition=community

Install the latest professional version:

.. code-block:: sh

    charmy install --edition=professional

Install specific version of the PyCharm. Let's assume the you want
to install community edition version 4.5.4:

.. code-block:: sh

    charmy install --version=4.5.4 --edition=community

Switch between installed PyCharm versions (imagine, you have both 4.5
and 4.5.4 installed and want to switch back to previous version):

.. code-block:: sh

    charmy activate --version=4.5 --edition=community

List installed PyCharm versions:

.. code-block:: sh

    charmy versions

By default `charmy` installs PyCharm in the `PyCharm` directory. If you want it
to be installed elsewhere provide --destination directive:

.. code-block:: sh

    charmy install --destination=/home/user/my-pycharm-installation-directory/

Note, that `charmy` remembers your last destination, so once you have
specified a destination, you don't have to specify it again (unless you
want to change installation directory).

Check for the latest available version (without installing it):

.. code-block:: sh

    charmy check-latest-available

Clear `charmy` settings (destination and the database drop):

.. code-block:: sh

    charmy reset-settings

Ubuntu
------
When installing on Ubuntu, `charmy` creates a `.desktop` file for to be drag
and dropped to the Unity launcher. The `.desktop` file is located at:

.. code-block:: html

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
