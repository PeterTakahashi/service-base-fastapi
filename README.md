# Image/Manga Translator

## Installation

### Local setup

#### Docker

```bash
docker exec -it manga-translator-web bash
source .venv/bin/activate

pytest
```

## Usage

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
