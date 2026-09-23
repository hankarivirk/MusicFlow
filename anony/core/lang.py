import json
import os

_languages = {}

def load_languages():
    locales_dir = os.path.join(os.path.dirname(__file__), "..", "locales")
    if not os.path.exists(locales_dir):
        return
    for f in os.listdir(locales_dir):
        if f.endswith(".json"):
            lang = f[:-5]
            with open(os.path.join(locales_dir, f), "r", encoding="utf-8") as fp:
                try:
                    _languages[lang] = json.load(fp)
                except Exception:
                    pass

def get_string(lang: str, key: str) -> str:
    if lang in _languages and key in _languages[lang]:
        return _languages[lang][key]
    if "en" in _languages and key in _languages["en"]:
        return _languages["en"][key]
    return key
