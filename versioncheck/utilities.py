from pathlib import Path
import os
#from env import Env

NEW_LINE_SEPARATOR = "\r\n"
LINE_FEED = "\n"

def check_env_variable(name, mandatory=True):
    """This function checks for Env variables"""
    var = os.environ.get(name)
    # if var is None:
    #     var = Env[name]
    if var is None and mandatory:
            print(f'Variable {name} not found!')
            exit(1)
    return var

def path_query(path: str, document: dict):
    """Retrieve json field"""
    dictionary_paths = Path(path)
    dictionary_keys = dictionary_paths.parts
    sub_document = None
    if len(dictionary_keys) > 1 or dictionary_keys[0] != '/':
        sub_document = document
    for key in dictionary_keys:
        if key != '/':
            sub_document = sub_document[key]
    return sub_document


def get_json_value(path: str, document: dict):
    # This function will return empty string if jason field not found.
    try:
        return path_query(path, document)
    except Exception:
        return None


def insert_str(string_value, str_to_insert, pos):
    """Insert a string in another at a specific position."""
    return string_value[:pos] + str_to_insert + string_value[pos:]


def get_string_position(content, string_value):
    """Retrieve a substring position in a string"""
    return content.find(string_value)


def modify_string_contents(contents, place, replacement):
    """Modify string contents setting a replacement at place position"""
    new_contents = None
    position = get_string_position(contents, place)
    old_line = contents[position:].replace(
        NEW_LINE_SEPARATOR, LINE_FEED
    ).split(LINE_FEED)[0]
    if f'{replacement}' not in old_line:
        new_contents = contents.replace(
            f'{old_line}',
            f'{place}{replacement}'
        )
    return new_contents


def retrieve_string_from_contents(contents, place):
    """Retrieve ending line form string contents at place position"""
    position = get_string_position(contents, place)
    if position == -1:
        return None
    value = contents[position:].replace(
        NEW_LINE_SEPARATOR, LINE_FEED
    ).split(LINE_FEED)[0].split(place)[1]
    return value

def log(*args):
    """Log message"""
    message = ''
    for arg in args:
        message = f'{message}{arg} '
    message = message[:-1]
    print(message)
