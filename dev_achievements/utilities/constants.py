# constant values to use throughout
import os


_ROOT_PATH = os.path.expanduser('~')
STORE_PATH = os.path.join(_ROOT_PATH, '.dev_achievements/store.json')


DEFAULT_STORE = {
    'unlocked': [],
}
