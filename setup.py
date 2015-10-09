import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '0.1.4'

exec_dirs = [
    'src/charmy/bin/',
]

execs = []
for exec_dir in exec_dirs:
    execs += [os.path.join(exec_dir, f) for f in os.listdir(exec_dir)]

install_requires = [
    'requests>=2.0',
    'argparse',
    'Flask>=0.10',
    'Flask-SQLAlchemy>=2.0',
    'six>=1.4',
]

setup(
    name = 'charmy',
    version = version,
    description = ("Automated PyCharm installer for Linux."),
    long_description=readme,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Topic :: Software Development",
        "Topic :: Text Editors :: Integrated Development Environments (IDE)",
    ],
    keywords = 'pycharm, installer',
    author = 'Artur Barseghyan',
    author_email = 'artur.barseghyan@gmail.com',
    url = 'https://github.com/barseghyanartur/charmy',
    package_dir = {'': 'src'},
    packages = find_packages(where='./src'),
    include_package_data = True,
    package_data = {
        'charmy': execs,
    },
    scripts = ['src/charmy/bin/charmy',],
    license = 'GPL 2.0/LGPL 2.1',
    install_requires = install_requires
)
