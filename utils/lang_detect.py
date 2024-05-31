from fast_langdetect import detect


def detect_french(text: str) -> bool:
    return detect(text)["lang"]


def detect_spanish(text: str) -> bool:
    return detect(text)["lang"]


print(
    detect_french(
        "Bonjour, je m'appelle Jean et c'est une phrase française sans ambiguïté."
    )
)
print(
    detect_spanish("Hola, me llamo Juan y esto es una frase en español sin ambigüedad.")
)
