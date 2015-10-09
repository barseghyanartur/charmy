__title__ = 'charmy.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'download_file', 'detect_latest_version',
)

import os
import re

import requests

from .constants import BASE_DIR, DOWNLOAD_PAGE_LINK, VERSION_JS_URL

def download_file(url, temp_dir, use_cache=True):
    """
    Downloads the file from given location and stores it locally. Returns
    the local filename (full path).

    :param str url: URL to download.
    :param str temp_dir: Full path to temporary directory to download files
                         to.
    :return str: Full path to the downloaded file.
    """
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    local_filename = os.path.join(
        os.path.dirname(BASE_DIR),
        temp_dir,
        url.split('/')[-1]
    )

    # Do not download if already downloaded.
    if os.path.isfile(local_filename) and use_cache:
        return local_filename

    # NOTE the stream=True parameter
    r = requests.get(url, stream=True, verify=False)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename

def detect_latest_version():
    """
    Detects the PyCharm latest version.

    :return:
    """
    response = requests.get(VERSION_JS_URL, verify=False)
    if response.ok:
        for line in response.iter_lines():
            if line.startswith('var versionPyCharmLong = '):
                version = re.search(
                    'var versionPyCharmLong = "(.*)";',
                    line,
                    re.IGNORECASE
                )
                if version:
                    return version.group(1)
