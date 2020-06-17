'''Compute our version number
'''

import pkg_resources


def getVersion(module=None):
    '''Get our own version using pkg_resources'''

    if module is None:
        module = 'wsproxy'

    return pkg_resources.get_distribution(module).version
