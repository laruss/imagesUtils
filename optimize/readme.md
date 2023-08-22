# Optimize Images

This submodule contains the scripts to optimize the images size and quality.

- [x] optimize images size
- [x] convert images to webp format
- [x] search for duplicates and similar images

## Installation

```bash
pip install -r requirements.txt
```

you can run the script with arguments or, changing the `./download/settings.py` file.

## How to use

```bash
python ./optimize/main.py --method to_webp --silent
python ./optimize/main.py --method minimize
```