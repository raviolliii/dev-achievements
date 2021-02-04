import json
import os
import pathlib

from dev_achievements.utilities.constants import STORE_PATH, DEFAULT_STORE


def load_json(file_path):
    """ Loads in a JSON file as a dict

    Args:
        file_path (str): path to JSON file

    Returns:
        dict: Data in file
    """
    data = {}
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def write_json(file_path, data):
    """ Writes given dict to a JSON file

    Args:
        file_path (str): path of JSON file
        data (dict): data to write
    """
    with open(file_path, 'w+') as file:
        json.dump(data, file, indent=4)
    return


def load_store(field=None):
    """ Loads in Achievement store as a dict. If a field value
    is specified, the data in the field is returned. If there
    is no file in the configured STORE_PATH, the configured
    DEFAULT_STORE is used.

    Args:
        field (str, optional): dictionary field
    
    Returns:
        The whole data store, or the data in the field if one is given.
    """
    store = DEFAULT_STORE
    # load in store if saved
    if os.path.isfile(STORE_PATH):
        store = load_json(STORE_PATH)
    # get field if specified
    if field is not None:
        return store.get(field, None)
    return store


def write_store(data):
    """ Writes given data to the Achievement store.

    Creates the full nested directory path of STORE_DIR
    if it doesn't exist, before writing/creating the store.

    Args:
        data (dict): updated Achievement store to write
    """
    store_dir = os.path.dirname(STORE_PATH)
    pathlib.Path(store_dir).mkdir(parents=True, exist_ok=True)
    return write_json(STORE_PATH, data)


def save_completed(ach_name):
    """ Marks the given Achievement as unlocked in the store.

    Args:
        ach_name (Achievement): class of Achievement
    """
    store = load_store()
    store['unlocked'].append(ach_name)
    write_store(store)
    return


def bordered(text):
    """ Pretty formats the given text in a solid box outline.

    Args:
        text (str): text within the box
    
    Returns:
        str: Boxed text
    """
    lines = text.splitlines()
    width = max([len(s) for s in lines])
    res = ['┌' + ('─' * (width + 2)) + '┐']
    for s in lines:
        sub = (s + (' ' * width))[:width]
        res.append('│ ' + sub + ' │')
    res.append('└' + ('─' * (width + 2)) + '┘')
    return '\n'.join(res)
