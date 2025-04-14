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
    - [Language Code Reference](#language-code-reference)
    - [Translators Reference](#translators-reference)
    - [Config file](#config-file)
    - [GPT Config Reference](#gpt-config-reference)
    - [Using Gimp for rendering](#using-gimp-for-rendering)

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
cd server && uvicorn main:app --reload --host 0.0.0.0 --port 8000
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

<!-- Auto generated end -->

### Language Code Reference

Used by the `translator/language` in the config

```yaml
CHS: Chinese (Simplified)
CHT: Chinese (Traditional)
CSY: Czech
NLD: Dutch
ENG: English
FRA: French
DEU: German
HUN: Hungarian
ITA: Italian
JPN: Japanese
KOR: Korean
PLK: Polish
PTB: Portuguese (Brazil)
ROM: Romanian
RUS: Russian
ESP: Spanish
TRK: Turkish
UKR: Ukrainian
VIN: Vietnames
ARA: Arabic
SRP: Serbian
HRV: Croatian
THA: Thai
IND: Indonesian
FIL: Filipino (Tagalog)
```

### Translators Reference

| Name          | API Key | Offline | Note                                                    |
| ------------- | ------- | ------- | ------------------------------------------------------- |
| <s>google</s> |         |         | Disabled temporarily                                    |
| youdao        | ✔️      |         | Requires `YOUDAO_APP_KEY` and `YOUDAO_SECRET_KEY`       |
| baidu         | ✔️      |         | Requires `BAIDU_APP_ID` and `BAIDU_SECRET_KEY`          |
| deepl         | ✔️      |         | Requires `DEEPL_AUTH_KEY`                               |
| caiyun        | ✔️      |         | Requires `CAIYUN_TOKEN`                                 |
| gpt3          | ✔️      |         | Implements text-davinci-003. Requires `OPENAI_API_KEY`  |
| gpt3.5        | ✔️      |         | Implements gpt-3.5-turbo. Requires `OPENAI_API_KEY`     |
| gpt4          | ✔️      |         | Implements gpt-4. Requires `OPENAI_API_KEY`             |
| papago        |         |         |                                                         |
| sakura        |         |         | Requires `SAKURA_API_BASE`                              |
| custom openai |         |         | Requires `CUSTOM_OPENAI_API_BASE` `CUSTOM_OPENAI_MODEL` |
| offline       |         | ✔️      | Chooses most suitable offline translator for language   |
| sugoi         |         | ✔️      | Sugoi V4.0 Models                                       |
| m2m100        |         | ✔️      | Supports every language                                 |
| m2m100_big    |         | ✔️      |                                                         |
| none          |         | ✔️      | Translate to empty texts                                |
| original      |         | ✔️      | Keep original texts                                     |

- API Key: Whether the translator requires an API key to be set as environment variable.
  For this you can create a .env file in the project root directory containing your api keys like so:

```env
OPENAI_API_KEY=sk-xxxxxxx...
DEEPL_AUTH_KEY=xxxxxxxx...
```

- Offline: Whether the translator can be used offline.

- Sugoi is created by mingshiba, please support him in https://www.patreon.com/mingshiba

### Config file

run `python -m manga_translator config-help >> config-info.json`

an example can be found in example/config-example.json

```json
{
  "$defs": {
    "Alignment": {
      "enum": ["auto", "left", "center", "right"],
      "title": "Alignment",
      "type": "string"
    },
    "Colorizer": {
      "enum": ["none", "mc2"],
      "title": "Colorizer",
      "type": "string"
    },
    "ColorizerConfig": {
      "properties": {
        "colorization_size": {
          "default": 576,
          "title": "Colorization Size",
          "type": "integer"
        },
        "denoise_sigma": {
          "default": 30,
          "title": "Denoise Sigma",
          "type": "integer"
        },
        "colorizer": {
          "$ref": "#/$defs/Colorizer",
          "default": "none"
        }
      },
      "title": "ColorizerConfig",
      "type": "object"
    },
    "Detector": {
      "enum": ["default", "dbconvnext", "ctd", "craft", "none"],
      "title": "Detector",
      "type": "string"
    },
    "DetectorConfig": {
      "properties": {
        "detector": {
          "$ref": "#/$defs/Detector",
          "default": "default"
        },
        "detection_size": {
          "default": 1536,
          "title": "Detection Size",
          "type": "integer"
        },
        "text_threshold": {
          "default": 0.5,
          "title": "Text Threshold",
          "type": "number"
        },
        "det_rotate": {
          "default": false,
          "title": "Det Rotate",
          "type": "boolean"
        },
        "det_auto_rotate": {
          "default": false,
          "title": "Det Auto Rotate",
          "type": "boolean"
        },
        "det_invert": {
          "default": false,
          "title": "Det Invert",
          "type": "boolean"
        },
        "det_gamma_correct": {
          "default": false,
          "title": "Det Gamma Correct",
          "type": "boolean"
        },
        "box_threshold": {
          "default": 0.7,
          "title": "Box Threshold",
          "type": "number"
        },
        "unclip_ratio": {
          "default": 2.3,
          "title": "Unclip Ratio",
          "type": "number"
        }
      },
      "title": "DetectorConfig",
      "type": "object"
    },
    "Direction": {
      "enum": ["auto", "horizontal", "vertical"],
      "title": "Direction",
      "type": "string"
    },
    "InpaintPrecision": {
      "enum": ["fp32", "fp16", "bf16"],
      "title": "InpaintPrecision",
      "type": "string"
    },
    "Inpainter": {
      "enum": ["default", "lama_large", "lama_mpe", "sd", "none", "original"],
      "title": "Inpainter",
      "type": "string"
    },
    "InpainterConfig": {
      "properties": {
        "inpainter": {
          "$ref": "#/$defs/Inpainter",
          "default": "none"
        },
        "inpainting_size": {
          "default": 2048,
          "title": "Inpainting Size",
          "type": "integer"
        },
        "inpainting_precision": {
          "$ref": "#/$defs/InpaintPrecision",
          "default": "fp32"
        }
      },
      "title": "InpainterConfig",
      "type": "object"
    },
    "Ocr": {
      "enum": ["32px", "48px", "48px_ctc", "mocr"],
      "title": "Ocr",
      "type": "string"
    },
    "OcrConfig": {
      "properties": {
        "use_mocr_merge": {
          "default": false,
          "title": "Use Mocr Merge",
          "type": "boolean"
        },
        "ocr": {
          "$ref": "#/$defs/Ocr",
          "default": "48px"
        },
        "min_text_length": {
          "default": 0,
          "title": "Min Text Length",
          "type": "integer"
        },
        "ignore_bubble": {
          "default": 0,
          "title": "Ignore Bubble",
          "type": "integer"
        }
      },
      "title": "OcrConfig",
      "type": "object"
    },
    "RenderConfig": {
      "properties": {
        "renderer": {
          "$ref": "#/$defs/Renderer",
          "default": "default"
        },
        "alignment": {
          "$ref": "#/$defs/Alignment",
          "default": "auto"
        },
        "disable_font_border": {
          "default": false,
          "title": "Disable Font Border",
          "type": "boolean"
        },
        "font_size_offset": {
          "default": 0,
          "title": "Font Size Offset",
          "type": "integer"
        },
        "font_size_minimum": {
          "default": -1,
          "title": "Font Size Minimum",
          "type": "integer"
        },
        "direction": {
          "$ref": "#/$defs/Direction",
          "default": "auto"
        },
        "uppercase": {
          "default": false,
          "title": "Uppercase",
          "type": "boolean"
        },
        "lowercase": {
          "default": false,
          "title": "Lowercase",
          "type": "boolean"
        },
        "gimp_font": {
          "default": "Sans-serif",
          "title": "Gimp Font",
          "type": "string"
        },
        "no_hyphenation": {
          "default": false,
          "title": "No Hyphenation",
          "type": "boolean"
        },
        "font_color": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Font Color"
        },
        "line_spacing": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Line Spacing"
        },
        "font_size": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Font Size"
        }
      },
      "title": "RenderConfig",
      "type": "object"
    },
    "Renderer": {
      "enum": ["default", "manga2eng", "none"],
      "title": "Renderer",
      "type": "string"
    },
    "Translator": {
      "enum": [
        "youdao",
        "baidu",
        "deepl",
        "papago",
        "caiyun",
        "gpt3",
        "gpt3.5",
        "gpt4",
        "none",
        "original",
        "sakura",
        "deepseek",
        "groq",
        "offline",
        "nllb",
        "nllb_big",
        "sugoi",
        "jparacrawl",
        "jparacrawl_big",
        "m2m100",
        "m2m100_big",
        "mbart50",
        "qwen2",
        "qwen2_big"
      ],
      "title": "Translator",
      "type": "string"
    },
    "TranslatorConfig": {
      "properties": {
        "translator": {
          "$ref": "#/$defs/Translator",
          "default": "sugoi"
        },
        "target_lang": {
          "default": "ENG",
          "title": "Target Lang",
          "type": "string"
        },
        "no_text_lang_skip": {
          "default": false,
          "title": "No Text Lang Skip",
          "type": "boolean"
        },
        "skip_lang": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Skip Lang"
        },
        "gpt_config": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Gpt Config"
        },
        "translator_chain": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Translator Chain"
        },
        "selective_translation": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Selective Translation"
        }
      },
      "title": "TranslatorConfig",
      "type": "object"
    },
    "UpscaleConfig": {
      "properties": {
        "upscaler": {
          "$ref": "#/$defs/Upscaler",
          "default": "esrgan"
        },
        "revert_upscaling": {
          "default": false,
          "title": "Revert Upscaling",
          "type": "boolean"
        },
        "upscale_ratio": {
          "anyOf": [
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "default": null,
          "title": "Upscale Ratio"
        }
      },
      "title": "UpscaleConfig",
      "type": "object"
    },
    "Upscaler": {
      "enum": ["waifu2x", "esrgan", "4xultrasharp"],
      "title": "Upscaler",
      "type": "string"
    }
  },
  "properties": {
    "filter_text": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "title": "Filter Text"
    },
    "render": {
      "$ref": "#/$defs/RenderConfig",
      "default": {
        "renderer": "default",
        "alignment": "auto",
        "disable_font_border": false,
        "font_size_offset": 0,
        "font_size_minimum": -1,
        "direction": "auto",
        "uppercase": false,
        "lowercase": false,
        "gimp_font": "Sans-serif",
        "no_hyphenation": false,
        "font_color": null,
        "line_spacing": null,
        "font_size": null
      }
    },
    "upscale": {
      "$ref": "#/$defs/UpscaleConfig",
      "default": {
        "upscaler": "esrgan",
        "revert_upscaling": false,
        "upscale_ratio": null
      }
    },
    "translator": {
      "$ref": "#/$defs/TranslatorConfig",
      "default": {
        "translator": "sugoi",
        "target_lang": "ENG",
        "no_text_lang_skip": false,
        "skip_lang": null,
        "gpt_config": null,
        "translator_chain": null,
        "selective_translation": null
      }
    },
    "detector": {
      "$ref": "#/$defs/DetectorConfig",
      "default": {
        "detector": "default",
        "detection_size": 1536,
        "text_threshold": 0.5,
        "det_rotate": false,
        "det_auto_rotate": false,
        "det_invert": false,
        "det_gamma_correct": false,
        "box_threshold": 0.7,
        "unclip_ratio": 2.3
      }
    },
    "colorizer": {
      "$ref": "#/$defs/ColorizerConfig",
      "default": {
        "colorization_size": 576,
        "denoise_sigma": 30,
        "colorizer": "none"
      }
    },
    "inpainter": {
      "$ref": "#/$defs/InpainterConfig",
      "default": {
        "inpainter": "none",
        "inpainting_size": 2048,
        "inpainting_precision": "fp32"
      }
    },
    "ocr": {
      "$ref": "#/$defs/OcrConfig",
      "default": {
        "use_mocr_merge": false,
        "ocr": "48px",
        "min_text_length": 0,
        "ignore_bubble": 0
      }
    },
    "kernel_size": {
      "default": 3,
      "title": "Kernel Size",
      "type": "integer"
    },
    "mask_dilation_offset": {
      "default": 0,
      "title": "Mask Dilation Offset",
      "type": "integer"
    }
  },
  "title": "Config",
  "type": "object"
}
```

### GPT Config Reference

Used by the `--gpt-config` argument.

```yaml
# The prompt being feed into GPT before the text to translate.
# Use {to_lang} to indicate where the target language name should be inserted.
# Note: ChatGPT models don't use this prompt.
prompt_template: >
  Please help me to translate the following text from a manga to {to_lang}
  (if it's already in {to_lang} or looks like gibberish you have to output it as it is instead):\n

# What sampling temperature to use, between 0 and 2.
# Higher values like 0.8 will make the output more random,
# while lower values like 0.2 will make it more focused and deterministic.
temperature: 0.5

# An alternative to sampling with temperature, called nucleus sampling,
# where the model considers the results of the tokens with top_p probability mass.
# So 0.1 means only the tokens comprising the top 10% probability mass are considered.
top_p: 1

# The prompt being feed into ChatGPT before the text to translate.
# Use {to_lang} to indicate where the target language name should be inserted.
# Tokens used in this example: 57+
chat_system_template: >
  You are a professional translation engine, 
  please translate the story into a colloquial, 
  elegant and fluent content, 
  without referencing machine translations. 
  You must only translate the story, never interpret it.
  If there is any issue in the text, output it as is.

  Translate to {to_lang}.

# Samples being feed into ChatGPT to show an example conversation.
# In a [prompt, response] format, keyed by the target language name.
#
# Generally, samples should include some examples of translation preferences, and ideally
# some names of characters it's likely to encounter.
#
# If you'd like to disable this feature, just set this to an empty list.
chat_sample:
  Simplified Chinese: # Tokens used in this example: 88 + 84
    - <|1|>恥ずかしい… 目立ちたくない… 私が消えたい…
      <|2|>きみ… 大丈夫⁉
      <|3|>なんだこいつ 空気読めて ないのか…？
    - <|1|>好尴尬…我不想引人注目…我想消失…
      <|2|>你…没事吧⁉
      <|3|>这家伙怎么看不懂气氛的…？

# Overwrite configs for a specific model.
# For now the list is: gpt3, gpt35, gpt4
gpt35:
  temperature: 0.3
```

### Using Gimp for rendering

When setting output format to {`xcf`, `psd`, `pdf`} Gimp will be used to generate the file.

On Windows this assumes Gimp 2.x to be installed to `C:\Users\<Username>\AppData\Local\Programs\Gimp 2`.

The resulting `.xcf` file contains the original image as the lowest layer and it has the inpainting as a separate layer.
The translated textboxes have their own layers with the original text as the layer name for easy access.

Limitations:

- Gimp will turn text layers to regular images when saving `.psd` files.
- Rotated text isn't handled well in Gimp. When editing a rotated textbox it'll also show a popup that it was modified
  by an outside program.
- Font family is controlled separately, with the `--gimp-font` argument.
