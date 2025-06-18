import json
from fastapi import Request
from pathlib import Path

messages = {}


def load_messages():
    global messages
    base_path = Path(__file__).parent.parent.parent / "locales"
    for path in base_path.glob("*.json"):
        lang = path.stem
        with open(path, encoding="utf-8") as f:
            messages[lang] = json.load(f)


def get_locale(request: Request) -> str:
    lang = request.headers.get("accept-language", "en").split(",")[0].lower()
    return lang


def get_message(locale: str, code: str, key: str) -> str:
    if not messages:
        load_messages()
    try:
        template = messages[locale][code][key]
    except KeyError:
        return ""

    return template
