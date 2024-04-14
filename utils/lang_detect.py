from langdetect import detect


def detect_french(text: str) -> bool:
    return detect(text) == "fr"


def detect_spanish(text: str) -> bool:
    return detect(text) == "es"
