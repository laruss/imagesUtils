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

Utils to upload images to cloud storages: [cloud](./cloud/readme.md) submodule.

Web interface for all modules: [web_interface](./web_interface/readme.md) submodule.

## TODO

- [x] replace print with logging
- [x] implement description module
- [x] implement cloud module
- [x] implement web interface
- [x] fix settings to use them in web interface
- [x] fix updating settings via web interface
- [x] fix http error to correspond to conventions
- [x] add response with info about processed method
- [x] fix core settings to transfer them from web server
- [ ] add methods dropdowns to web interface (front)
- [ ] validate data forms before sending to server (front)
- [ ] use Celery for long tasks (all images methods)
- [ ] add docker support
