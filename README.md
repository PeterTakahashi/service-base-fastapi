# Image/Manga Translator

Some manga/images will never be translated, therefore this project is born.

- [Image/Manga Translator](#imagemanga-translator)
  - [Installation](#installation)
    - [Local setup](#local-setup)
      - [Pip/venv](#pipvenv)
  - [Usage](#usage)
    - [Web Mode](#web-mode)
  - [Docs](#docs)
    - [Tips to improve translation quality](#tips-to-improve-translation-quality)
    - [Options](#options)

## Installation

### Local setup

#### Pip/venv

```bash
python --version
# Python 3.10.16

# Create venv
python -m venv venv

# Activate venv
source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

pytest test
```

## Usage

### Web Mode

```bash
# use `--mode web` to start a web server.
python -m manga_translator shared --port 8001 --use-gpu --font-path fonts/anime_ace_3.ttf
cd app && uvicorn main:app --reload --host 0.0.0.0 --port 8000
# the demo will be serving on http://127.0.0.1:5003
```

## Docs

#### Tips to improve translation quality

- Small resolutions can sometimes trip up the detector, which is not so good at picking up irregular text sizes. To
  circumvent this you can use an upscaler by specifying `--upscale-ratio 2` or any other value
- If the text being rendered is too small to read specify `--font-size-minimum 30` for instance or use the `--manga2eng`
  renderer that will try to adapt to detected textbubbles
- Specify a font with `--font-path fonts/anime_ace_3.ttf` for example

### Options

```text
-h, --help                     show this help message and exit
-v, --verbose                  Print debug info and save intermediate images in result folder
--attempts ATTEMPTS            Retry attempts on encountered error. -1 means infinite times.
--ignore-errors                Skip image on encountered error.
--model-dir MODEL_DIR          Model directory (by default ./models in project root)
--use-gpu                      Turn on/off gpu (auto switch between mps and cuda)
--use-gpu-limited              Turn on/off gpu (excluding offline translator)
--font-path FONT_PATH          Path to font file
--pre-dict PRE_DICT            Path to the pre-translation dictionary file
--post-dict POST_DICT          Path to the post-translation dictionary file
--kernel-size KERNEL_SIZE      Set the convolution kernel size of the text erasure area to
                               completely clean up text residues
--config-file CONFIG_FILE      path to the config file
--models-ttl MODELS_TTL        How long to keep models in memory in seconds after last use (0 means
                               forever)
```
