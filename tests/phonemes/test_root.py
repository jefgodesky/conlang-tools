from phonemes.roots import Syllable


class TestSyllable:
    def test_creates_syllable(self):
        syllable = Syllable("/ba/")
        assert isinstance(syllable, Syllable)

    def test_takes_ipa(self):
        syllable = Syllable("/ba/")
        assert syllable.ipa == "/ba/"

    def test_captures_stress(self):
        stressed = Syllable("/ˈba/")
        unstressed = Syllable("/ba/")
        assert stressed.stressed is True
        assert unstressed.stressed is False

    def test_breaks_down_phonemes(self):
        syllable = Syllable("/ba/")
        assert len(syllable.phonemes) == 2
        assert syllable.phonemes[0].symbol == "b"
        assert syllable.phonemes[1].symbol == "a"

    def test_unbrackets_ipa(self):
        syllable = Syllable("/ˈba/")
        assert syllable.unbracketed == "ˈba"

    def test_unmarked_ipa(self):
        syllable = Syllable("/ˈba/")
        assert syllable.unmarked == "ba"
