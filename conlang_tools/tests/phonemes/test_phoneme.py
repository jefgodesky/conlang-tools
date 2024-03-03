from conlang_tools.phonemes.phonemes import Phoneme


class TestPhoneme:
    def test_creates_phoneme(self):
        p = Phoneme("a")
        assert isinstance(p, Phoneme)
        assert p.symbol == "a"

    def test_repr(self):
        a = Phoneme("a")
        assert str(a) == "[a]"
