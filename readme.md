# About

These are some utils for working with images to represent them as some data.

Main data model is `core/ProcessedItem.py` class. It contains all data about image.

## Installation

```bash
pip install -r requirements.txt
```

*if you are going use `description` submodule with _describe_ module and `transformers`, 
you need to install `pytorch` package for your system.* 
(more info: [pytorch.org](https://pytorch.org/get-started/locally/))

## Modules

Utils to download images: [download](./download/readme.md) submodule.

Utils to optimize images: [optimize](./optimize/readme.md) submodule.

Utils to create images descriptions: [description](./description/readme.md) submodule.

## TODO

- [x] replace print with logging
- [x] implement description module
- [ ] implement cloud module
- [ ] implement web interface
