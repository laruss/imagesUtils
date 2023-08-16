from __future__ import print_function

import os.path
from enum import Enum
from typing import List, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from cloud import settings
from core.utils import get_logger

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

logger = get_logger()


class MimeTypes(Enum):
    FOLDER = "application/vnd.google-apps.folder"
    IMAGE = "image/jpeg"
    ZIP = "application/zip"


class File:
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

    def __str__(self):
        return f"File(name={self.name}, id={self.id})"


class GoogleDriveClient:
    mimetypes = MimeTypes

    def __init__(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=settings.google.local_server_port)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)

        logger.info("Google Drive client initialized")

    def list_files(self,
                   page_size: int = None,
                   page_token: str = None,
                   query: str = None,
                   spaces: str = 'drive'
                   ) -> (List[File], Optional[str]):
        results = self.service.files().list(
            pageSize=page_size,
            fields="nextPageToken, files(id, name)",
            pageToken=page_token,
            q=query,
            spaces=spaces
        ).execute()
        logger.info(f"Found {len(results.get('files', []))} files")

        items = results.get('files', [])

        files = [File(item['name'], item['id']) for item in items]

        return files, results.get('nextPageToken', None)

    def create_folder(self, name: str) -> File:
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        file = self.service.files().create(body=file_metadata, fields='id').execute()
        file_id = file.get('id')

        logger.info(f"Created folder {name} with id {file_id}")

        return File(name, file_id)

    def search_for_file_by_name(self, name: str, file_mime: MimeTypes) -> List[File]:
        files = []
        page_token = None
        query = f"mimeType='{file_mime.value}' and name contains '{name}'"

        logger.info(f"Searching for {name} with mime {file_mime.value}")
        while True:
            _files, page_token = self.list_files(page_token=page_token, query=query)
            files.extend(_files)

            if page_token is None:
                break

        logger.info(f"Found {len(files)} files")

        return files

    def create_folder_if_not_exists(self, name: str) -> File:
        logger.info(f"Creating folder if not exists: {name}")
        files = self.search_for_file_by_name(name, self.mimetypes.FOLDER)

        if len(files) == 0:
            logger.info(f"Folder {name} doesn't exist, creating")
            return self.create_folder(name)

        logger.info(f"Folder {name} already exists, skipping")

        return files[0]

    def upload_to_folder(self,
                         folder: File,
                         file_path: str,
                         file_mime: MimeTypes,
                         file_name: str = None
                         ) -> File:
        file_name = file_name or os.path.basename(file_path)

        logger.info(f"Uploading {file_name} to {folder.name}")

        file_metadata = {
            'name': file_name,
            'parents': [folder.id]
        }

        media = MediaFileUpload(file_path, mimetype=file_mime.value, resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        logger.info(f"Uploaded {file_name} to {folder.name}")

        return File(file_name, file.get('id'))

    def download_file(self, file: File, file_path: str):
        logger.info(f"Downloading {file.name} to {file_path}")
        request = self.service.files().get_media(fileId=file.id)
        fh = open(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            logger.info(f"Download {int(status.progress() * 100)}%.")

        logger.info(f"Downloaded {file.name} to {file_path}")

    def delete_file(self, file: File):
        logger.info(f"Deleting {file.name}")
        self.service.files().delete(fileId=file.id).execute()

        logger.info(f"Deleted {file.name}")

    def upload_zip_to_folder_name(self,
                                  folder_name: str,
                                  file_path: str,
                                  delete_if_exists: bool = True
                                  ) -> File:
        assert len(self.search_for_file_by_name(folder_name, self.mimetypes.FOLDER)) <= 1, \
            "More than one folder with the same name, please use a unique name"
        folder = self.create_folder_if_not_exists(folder_name)
        file_name = file_path.split("/")[-1]

        if delete_if_exists:
            files = self.search_for_file_by_name(file_name, self.mimetypes.ZIP)
            if len(files) > 0:
                self.delete_file(files[0])

        return self.upload_to_folder(folder, file_path, self.mimetypes.ZIP, file_name)

    def download_zip_from_folder_name(self, folder_name: str, file_path: str):
        folders = self.search_for_file_by_name(folder_name, self.mimetypes.FOLDER)
        file_name = file_path.split("/")[-1]

        assert len(folders) == 1, f"Folders with name {folder_name} not found or more than one found ({len(folders)} found)"

        file = self.search_for_file_by_name(file_name, self.mimetypes.ZIP)

        assert len(file) == 1, f"Zip file with name {file_name} not found or more than one found ({len(file)} found)"

        self.download_file(file[0], file_path)
