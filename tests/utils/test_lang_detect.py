from conversa.utils.lang_detect import detect_french, detect_spanish


class TestLangDetect:
    # test positive case (full french sentence)
    def test_detect_french(self):
        assert (
            detect_french(
                "Bonjour, je m'appelle Jean et c'est une phrase française sans ambiguïté."
            )
            == True
        )
