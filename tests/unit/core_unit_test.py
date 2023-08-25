import unittest
from unittest.mock import Mock, patch

import requests

from core.images_utils import (
    get_image_path_by_id,
    get_id_by_image_path,
    delete_image_data,
    download_from_url,
)
from core.utils import create_folder_if_not_exists, write_to_file, read_from_file

path = "/test/path"
image_id = "test"
image_name = "test.jpg"
image_path = f"{path}/{image_name}"


class CoreUnitTest(unittest.TestCase):
    @patch("core.images_utils.glob", new_callable=Mock)
    def test_get_image_path_by_id(self, mocked_glob):
        mocked_glob.glob.return_value = [image_path]
        self.assertEquals(
            get_image_path_by_id(image_id, path), image_path, "Should return image path"
        )

        mocked_glob.glob.return_value = []
        kwargs = [
            {"image_id": image_id, "images_folder_path": path},
            {"image_id": image_id, "images_folder_path": None},
            {"image_id": None, "images_folder_path": path},
        ]

        for kwarg in kwargs:
            self.assertIsNone(
                get_image_path_by_id(**kwarg),
                "Should return None if image path not found",
            )

    def test_get_id_by_image_path(self):
        self.assertEquals(
            get_id_by_image_path(image_path),
            image_id,
            "Should return image id from image path",
        )
        self.assertEquals(
            get_id_by_image_path(image_id),
            image_id,
            "Should return image id from image id",
        )

        with self.assertRaises(TypeError):
            get_id_by_image_path(None)

    @patch("core.images_utils.write_json_to_file", new_callable=Mock)
    @patch("core.images_utils.read_json_from_file", new_callable=Mock)
    @patch("core.images_utils.os", new_callable=Mock)
    @patch("core.images_utils.glob", new_callable=Mock)
    def test_delete_image_data(
        self,
        mocked_glob,
        mocked_os,
        mocked_read_json_from_file,
        mocked_write_json_to_file,
    ):
        mocked_glob.glob.return_value = [image_path]
        mocked_os.remove.return_value = None
        mocked_read_json_from_file.return_value = {image_id: {}}
        mocked_write_json_to_file.return_value = None

        self.assertIsNone(delete_image_data(image_id, path, path), "Should return None")

        mocked_glob.glob.return_value = []
        mocked_read_json_from_file.return_value = {image_id: {}}
        self.assertIsNone(
            delete_image_data(image_id, path, path),
            "Should return None if image path not found",
        )
        mocked_write_json_to_file.assert_called_with({}, path, rewrite=True)

        mocked_read_json_from_file.return_value = {}
        with self.assertRaises(KeyError):
            delete_image_data(image_id, path, path)

    @patch("core.images_utils.Image", new_callable=Mock)
    @patch("core.images_utils.requests", new_callable=Mock)
    def test_download_from_url(self, mocked_requests, mocked_Image):
        url = "https://test.com/test.jpg"

        mocked_requests.get.return_value = Mock(content="test")
        mocked_Image.open.return_value = Mock(save=Mock(), convert=Mock(), close=Mock())

        [
            self.assertTrue(
                download_from_url(url, image_path, fall_on_fail), "Should return True"
            )
            for fall_on_fail in [True, False]
        ]

        mocked_requests.get.side_effect = requests.exceptions.RequestException

        for fall_on_fail in [True, False]:
            if fall_on_fail:
                with self.assertRaises(requests.exceptions.RequestException):
                    download_from_url(url, image_path, fall_on_fail)
            else:
                self.assertFalse(
                    download_from_url(url, image_path, fall_on_fail),
                    "Should return False",
                )

    @patch("core.utils.os", new_callable=Mock)
    def test_create_folder_if_not_exists(self, mocked_os):
        mocked_os.path.exists.return_value = True
        mocked_os.makedirs.return_value = None

        self.assertIsNone(create_folder_if_not_exists(path), "Should return None")

        mocked_os.path.exists.return_value = False
        self.assertIsNone(create_folder_if_not_exists(path), "Should return None")
        mocked_os.makedirs.assert_called_with(path, exist_ok=True)

    @patch("core.utils.os", new_callable=Mock)
    @patch("builtins.open", new_callable=Mock)
    def test_write_to_file(self, mocked_open, mocked_os):
        mocked_open.return_value = Mock(
            write=Mock(), close=Mock(), __enter__=Mock(), __exit__=Mock()
        )
        mocked_os.path.dirname.return_value = path

        mocked_os.path.isFile.return_value = True
        mocked_os.path.exists.return_value = True
        mocked_os.makedirs.return_value = None

        with self.assertRaises(ValueError):
            write_to_file(data=None, path=path)

        mocked_os.path.exists.side_effect = TypeError
        with self.assertRaises(TypeError):
            write_to_file(data="test", path=None)

        mocked_os.path = Mock(isfile=Mock(return_value=False))
        with self.assertRaises(ValueError):
            write_to_file(data="test", path="test")

        mocked_os.path = Mock(exists=Mock(return_value=False))
        with self.assertRaises(FileNotFoundError):
            write_to_file(data="test", path="test", create_if_not_exist=False)

        mocked_os.path = Mock(
            exists=Mock(return_value=True), isfile=Mock(return_value=True)
        )
        self.assertIsNone(
            write_to_file(data="test", path="test", rewrite=True), "Should return None"
        )
        mocked_open.assert_called_with("test", "w")

        self.assertIsNone(
            write_to_file(data="test", path="test", rewrite=False), "Should return None"
        )
        mocked_open.assert_called_with("test", "a")

        mocked_os.path = Mock(exists=Mock(return_value=False))
        mocked_os.path.dirname.return_value = path
        self.assertIsNone(
            write_to_file(data="test", path="test", create_if_not_exist=True),
            "Should return None",
        )
        mocked_os.makedirs.assert_called_with(path, exist_ok=True)

    @patch("builtins.open", new_callable=Mock)
    @patch("core.utils.os", new_callable=Mock)
    def test_read_from_file(self, mocked_os, mocked_open):
        mocked_open.return_value = Mock(
            close=Mock(),
            __enter__=Mock(return_value=Mock(read=Mock(return_value="test"))),
            __exit__=Mock(),
        )
        mocked_os.path.exists.return_value = True
        mocked_os.path.isfile.return_value = False

        with self.assertRaises(FileNotFoundError):
            read_from_file(path)

        mocked_os.path.exists.return_value = False
        mocked_os.path.isfile.return_value = True

        with self.assertRaises(FileNotFoundError):
            read_from_file(path)

        mocked_os.path.exists.return_value = True
        mocked_os.path.isfile.return_value = True

        self.assertEquals(read_from_file(path), "test", "Should return data from file")
        mocked_open.assert_called_with(path, "r")
