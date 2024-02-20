from phonemes.phonemes import get_phoneme
from phonemes.roots import Root, Syllable


class TestRoot:
    def test_creates_root(self):
        root = Root("/ˈba.ba/")
        assert isinstance(root, Root)

    def test_takes_ipa(self):
        root = Root("/ˈba.ba/")
        assert root.ipa == "/ˈba.ba/"

    def test_breaks_down_syllables(self):
        root = Root("/ˈba.ba/")
        assert len(root.syllables) == 2
        assert all([isinstance(syllable, Syllable) for syllable in root.syllables])
        assert root.syllables[0].stressed is True
        assert root.syllables[1].stressed is False

    def test_rebuild(self):
        root = Root("/ˈba.ba/")
        root.syllables[0].phonemes[0] = get_phoneme("k")
        root.syllables[1].phonemes[0] = get_phoneme("l")
        root.rebuild()
        assert root.ipa == "/ˈka.la/"

    def test_phonemes(self):
        root = Root("/ˈba.ba/")
        symbols = [p.symbol for p in root.phonemes]
        assert "".join(symbols) == "baba"


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
        syllable = Syllable("/ba:/")
        assert len(syllable.phonemes) == 2
        assert syllable.phonemes[0].symbol == "b"
        assert syllable.phonemes[1].symbol == "a:"
        assert syllable.phonemes[1].long is True

    def test_unbrackets_ipa(self):
        syllable = Syllable("/ˈba/")
        assert syllable.unbracketed == "ˈba"

    def test_unmarked_ipa(self):
        syllable = Syllable("/ˈba/")
        assert syllable.unmarked == "ba"

    def test_rebuild(self):
        syllable = Syllable("/ˈba/")
        syllable.phonemes[0] = get_phoneme("k")
        syllable.rebuild()
        assert syllable.ipa == "/ˈka/"
