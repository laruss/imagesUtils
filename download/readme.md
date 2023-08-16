# Download images

This submodule contains the scripts to download the images from some resources such as google, pexels, etc.

## Installation

```bash
pip install -r requirements.txt
```

change the `./download/.env.sample` to `./download/.env` and fill all the needed fields.

you can run the script with arguments or, changing the `./download/settings.py` file.

## How to use

```bash
python ./download/main.py --source google --limit 10 --prompt "cat"
```

All images will be downloaded to the `./static/images` folder.

Also, there will be created a `./static/data.json` file with images data.

# Adding new resource

## How to create response pydantic model

1. Make a valid request to resource API (using postman, curl, etc.)
2. Save the response to the JSON file (e.g. `./download/resources/google/response.json`)
3. Run the `datamodel-codegen` command to generate the pydantic model

```bash
datamodel-codegen --input ./download/resources/google/response.json --output ./download/resources/google/response.py
```

4. Move model to the `download/models` folder
5. Create controller module in the `download/controllers` folder
6. Change `download/main.py` (`download/settings.py` and `download/.env.sample` files (if needed))
7. Run and test the script
8. Profit!