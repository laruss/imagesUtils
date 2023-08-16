# Describe images in data file and some other description stuff

This submodule contains the scripts to describe the images from the `./static/images` folder.

## Installation

```bash
pip install -r requirements.txt
```

change the `./description/.env.sample` to `./description/.env` and fill all the needed fields.

you can run the script with arguments or, changing the `./download/settings.py` file.

*if you are going use _describe_ module and `transformers`, you need to install `pytorch` package for your system.* 
(more info: [pytorch.org](https://pytorch.org/get-started/locally/))

## How to use

```bash
python ./description/main.py --method describe --silent
python ./description/main.py --method delete_nsfw
python ./description/main.py --method gpt --gpt-model "gpt-4" --used-gpt openai
python ./description/main.py --method gpt2json
```

## Additional info

describe method will update a `data.json` file with images description. You can use 2 methods, that can be set in the `./description/settings.py` file:
- `replicate` - will use [replicate.com](https://replicate.com/) API to describe images
- `transformers` - will use [transformers](https://huggingface.co/transformers/) library to describe images (locally)

delete_nsfw method will delete all images with NSFW content (NSFW defined by [sightengine.com](https://sightengine.com/) API)

gpt method will describe images using [openai.com](https://openai.com/) API. You can use 2 libraries:
- `openai` - will use [openai.com](https://openai.com/) API and library
- `g4f` - will use [g4f](https://github.com/xtekky/gpt4free) library

the prompt for the gpt method can be set in the `./description/prompts.py` file.

also you can set gpt model:
- `gpt-4` - will use [gpt-4](https://platform.openai.com/docs/models/gpt-4) model
- `gpt-3.5-turbo` - will use [gpt-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5) model

gpt2json method will convert gpt description to the json format. (locally)

all additional settings can be set in the `./description/settings.py` file.
