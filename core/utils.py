import json
import os
from typing import Union, Any


def get_root_path():
    return os.path.dirname(os.path.abspath(__file__) + '/../')


def write_to_file(
        data,
        path: str,
        create_if_not_exist: bool = True,
        rewrite: bool = False,
        silent: bool = False
):
    """
    Writes data to a file.

    :param data: some data to write
    :param path: path to the file
    :param create_if_not_exist: boolean, whether to create the file if it does not exist
    :param rewrite: boolean, whether to rewrite the file if it exists
    :param silent: boolean, whether to print a message after writing
    :return: None
    """
    if os.path.exists(path) and not os.path.isfile(path):
        raise ValueError(f"The path '{path}' is not a file.")

    if not os.path.exists(path):
        if create_if_not_exist:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as _:
                pass
        else:
            raise FileNotFoundError(f"The file '{path}' does not exist.")

    mode = 'w' if rewrite else 'a'
    with open(path, mode) as file:
        file.write(data)

    if not silent:
        print(f"Data successfully written to '{path}'.")


def read_from_file(path: str, silent: bool = True) -> Any:
    """
    Reads data from a file.

    :param path: path to the file
    :param silent: boolean, whether to print a message after reading
    :return: data from the file, any type
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")

    with open(path, 'r') as file:
        data = file.read()

    if not silent:
        print(f"Data successfully read from '{path}'.")

    return data


def write_json_to_file(
        data: Union[dict, list],
        path: str,
        create_if_not_exist: bool = True,
        rewrite: bool = False,
        silent: bool = False
):
    """
    Writes JSON data to a file.
    :param data: dict or list
    :param path: path to the json file
    :param create_if_not_exist: boolean, whether to create the file if it does not exist
    :param rewrite: boolean, whether to rewrite the file if it exists
    :param silent: boolean, whether to print a message after writing
    :return: None
    """
    write_to_file(json.dumps(data, indent=4), path, create_if_not_exist, rewrite, silent)


def read_json_from_file(path: str, silent=False) -> Union[dict, list]:
    """
    Reads JSON data from a file.

    :param path: path to the json file
    :param silent: boolean, whether to print a message after writing
    :return: dict or list
    """
    file_content = read_from_file(path, silent=silent)

    try:
        data = json.loads(file_content)
    except json.JSONDecodeError:
        raise ValueError(f"The file '{path}' does not contain valid JSON.")

    return data
