import pytest

from phonemes.consonants import Consonant
from phonemes.vowels import Vowel
from phonemes.phonemes import get_phoneme
from phonemes.roots import Root, Syllable


class TestRoot:
    @pytest.fixture
    def example_root(self):
        return Root("/ˈba.ba/")

    def test_creates_root(self, example_root):
        assert isinstance(example_root, Root)

    def test_takes_ipa(self, example_root):
        assert example_root.ipa == "/ˈba.ba/"

    def test_breaks_down_syllables(self, example_root):
        assert len(example_root.syllables) == 2
        assert all(
            [isinstance(syllable, Syllable) for syllable in example_root.syllables]
        )
        assert example_root.syllables[0].stressed is True
        assert example_root.syllables[1].stressed is False

    def test_rebuild(self, example_root):
        example_root.syllables[0].phonemes[0] = get_phoneme("k")
        example_root.syllables[1].phonemes[0] = get_phoneme("l")
        example_root.rebuild()
        assert example_root.ipa == "/ˈka.la/"

    def test_phonemes(self, example_root):
        symbols = [p.symbol for p in example_root.phonemes]
        assert "".join(symbols) == "baba"

    def test_phoneme_index(self, example_root):
        index = example_root.phoneme_index
        expectations = [
            (0, 0, Consonant, "b"),
            (0, 1, Vowel, "a"),
            (1, 0, Consonant, "b"),
            (1, 1, Vowel, "a"),
        ]

        for i, item in enumerate(index):
            assert item[0] == expectations[i][0]
            assert item[1] == expectations[i][1]
            assert isinstance(item[2], expectations[i][2])
            assert item[2].symbol == expectations[i][3]

    def test_preceding_found(self, example_root):
        actual = example_root.preceding(1, 0)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "a"

    def test_preceding_not_found(self, example_root):
        assert example_root.preceding(0, 0) is None

    def test_following_found(self, example_root):
        actual = example_root.following(0, 1)
        assert isinstance(actual, Consonant)
        assert actual.symbol == "b"

    def test_following_not_found(self, example_root):
        assert example_root.following(1, 1) is None


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
