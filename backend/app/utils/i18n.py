# Поддержка языков
translations = {
    "en": {
        "energy": "Energy",
        "gems": "Gems",
        "not_enough_energy": "Not enough energy",
        "shop": "Shop",
        "buy": "Buy"
    },
    "ru": {
        "energy": "Энергия",
        "gems": "Гемы",
        "not_enough_energy": "Не хватает энергии",
        "shop": "Магазин",
        "buy": "Купить"
    },
    "ja": {
        "energy": "エネルギー",
        "gems": "ジェム",
        "not_enough_energy": "エネルギー不足",
        "shop": "ショップ",
        "buy": "購入"
    }
}

def get_text(lang: str, key: str) -> str:
    return translations.get(lang, translations["en"]).get(key, key)