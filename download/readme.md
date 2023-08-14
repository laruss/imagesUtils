# Download images

This submodule contains the scripts to download the images from some resources such as google, pexels, etc.

## Installation

```bash
pip install -r requirements.txt
```

change the `./download/.env.sample` to `./download/.env` and fill all the required fields.

you can run the script with arguments or, changing the `./download/settings.py` file.

## How to use

```bash
python ./download/main.py --source google --limit 10 --prompt "cat"
```

All images will be downloaded to the `./static/images` folder.

Also, there will be created a `./static/data.json` file with images data.