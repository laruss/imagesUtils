import json
import logging
import os
import pathlib
from typing import Union, Any


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_logger() -> logging.Logger:
    logger_ = logging.getLogger("images-utils")

    return logger_


logger = get_logger()


def get_root_path():
    return pathlib.Path(__file__).parent.parent.resolve()


def set_logger(state: bool = True, filename: str = None):
    """
    Sets the logger state.

    :param state: boolean, whether to switch the logger on or off
    :param filename: path to the log file, if None, the log will be printed to the console
    :return: None
    """
    if not state:
        logger.setLevel(logging.CRITICAL + 1)

    if filename is not None:
        handler = logging.FileHandler(filename)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)


def create_folder_if_not_exists(path: str) -> None:
    """
    Creates a folder if it does not exist.

    :param path: path to the folder
    :return: None
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        logger.info(f"Folder '{path}' was created.")


def write_to_file(
    data, path: str, create_if_not_exist: bool = True, rewrite: bool = False
):
    """
    Writes data to a file.

    :param data: some data to write
    :param path: path to the file
    :param create_if_not_exist: boolean, whether to create the file if it does not exist
    :param rewrite: boolean, whether to rewrite the file if it exists
    :return: None
    """
    if os.path.exists(path) and not os.path.isfile(path):
        raise ValueError(f"The path '{path}' is not a file.")

    if not os.path.exists(path):
        if create_if_not_exist:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as _:
                pass
        else:
            raise FileNotFoundError(f"The file '{path}' does not exist.")

    mode = "w" if rewrite else "a"
    with open(path, mode) as file:
        file.write(data)

    logger.info(f"Data successfully written to '{path}'.")


def read_from_file(path: str) -> Any:
    """
    Reads data from a file.

    :param path: path to the file
    :return: data from the file, any type
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")

    with open(path, "r") as file:
        data = file.read()

    logger.info(f"Data successfully read from '{path}'.")

    return data


def write_json_to_file(
    data: Union[dict, list],
    path: str,
    create_if_not_exist: bool = True,
    rewrite: bool = False,
):
    """
    Writes JSON data to a file.
    :param data: dict or list
    :param path: path to the json file
    :param create_if_not_exist: boolean, whether to create the file if it does not exist
    :param rewrite: boolean, whether to rewrite the file if it exists
    :return: None
    """
    write_to_file(json.dumps(data, indent=4), path, create_if_not_exist, rewrite)


def read_json_from_file(
    path: str, error_on_invalid_json=True
) -> Union[dict, list, None]:
    """
    Reads JSON data from a file.

    :param path: path to the json file
    :param error_on_invalid_json: whether to raise an error if the file does not contain valid JSON or not exists
    :return: dict or list
    """
    try:
        file_content = read_from_file(path)
        data = json.loads(file_content)
    except Exception as e:
        if error_on_invalid_json:
            raise e
        else:
            data = None

    return data


def delete_file(path: str) -> None:
    """
    Deletes a file.

    :param path: path to the file
    :return: None
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        raise FileNotFoundError(f"The file '{path}' does not exist.")

    os.remove(path)
    logger.info(f"File '{path}' was deleted.")
