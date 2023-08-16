# Upload static files to cloud storage

This submodule contains the scripts to upload the static files to the cloud storage.

## Installation

```bash
pip install -r requirements.txt
```

change the `./cloud/.env.sample` to `./cloud/.env` and fill all the needed fields.

you can run the script with arguments or, changing the `./cloud/settings.py` file.

### Google Drive

To use Google Drive API you need to create a project in the [Google Cloud Console](https://console.cloud.google.com/).

Instructions [here](https://developers.google.com/drive/api/quickstart/python).

*WARN: make sure you set the application to test status [here](https://console.cloud.google.com/apis/credentials/consent).*

Make sure you set free local port in `./cloud/settings.py` file and then set it in the Google Cloud Console 
[Credentials page](https://console.cloud.google.com/apis/credentials).

Then you need to download the credentials file from the Google Cloud Console.

After downloading the credentials file, you need to move it to the `./cloud` folder, name it `credentials.json`.

### Yandex Disk

To use Yandex Disk API you need to create a project in the [Yandex Cloud Console](https://console.cloud.yandex.ru/).

Instructions [here](https://habr.com/ru/articles/749156/).

*(For english versions, please consider using Google Translate)*

Create API key and copy it to the `./cloud/.env` file.

Profit.

## How to use

```bash
python ./cloud/main.py --source google --method upload
python ./cloud/main.py --source yandex --method download
```
