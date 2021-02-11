# constants.py
# ------------
# Just a bunch of constants values for use throughout the codebase.

import os


# Achievement store path
_ROOT_PATH = os.path.expanduser('~')
STORE_PATH = os.path.join(_ROOT_PATH, '.dev_achievements/store.json')


# default Achievement store data
DEFAULT_STORE = {
    'unlocked': [],
}
