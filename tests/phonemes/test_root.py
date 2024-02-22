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

    def test_stresses_stressed_syllables(self, example_root):
        assert example_root.stresses(0) is True

    def test_does_not_stress_unstressed_syllables(self, example_root):
        assert example_root.stresses(1) is False

    def test_stresses_isolated_syllables(self):
        root = Root("/ba/")
        assert root.stresses(0) is True

    def test_rebuild(self, example_root):
        example_root.syllables[0].phonemes[0] = get_phoneme("k")
        example_root.syllables[1].phonemes[0] = get_phoneme("l")
        example_root.rebuild()
        assert example_root.ipa == "/ˈka.la/"

    def test_rebuild_cleans_up_orphan_syllables(self):
        r1 = Root("/ˈba.ba.b/")
        r2 = Root("/ˈba.b/")

        r1.rebuild()
        r2.rebuild()

        assert r1.ipa == "/ˈba.bab/"
        assert r2.ipa == "/bab/"

    def test_rebuild_does_not_mark_sole_syllable(self):
        root = Root("/ˈba.ba/")
        root.syllables = [root.syllables[0]]
        root.rebuild()
        assert root.ipa == "/ba/"

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

    def test_neighbors_both_found(self, example_root):
        neighbors = example_root.neighbors(0, 1)
        assert len(neighbors) == 2
        for neighbor in neighbors:
            assert isinstance(neighbor, Consonant)
            assert neighbor.symbol == "b"

    def test_neighbors_preceding_found(self, example_root):
        neighbors = example_root.neighbors(1, 1)
        assert len(neighbors) == 2
        assert isinstance(neighbors[0], Consonant)
        assert neighbors[0].symbol == "b"
        assert neighbors[1] is None

    def test_neighbors_following_found(self, example_root):
        neighbors = example_root.neighbors(0, 0)
        assert len(neighbors) == 2
        assert neighbors[0] is None
        assert isinstance(neighbors[1], Vowel)
        assert neighbors[1].symbol == "a"

    def test_neighbors_not_found(self):
        root = Root("/a/")
        neighbors = root.neighbors(0, 0)
        assert len(neighbors) == 2
        assert neighbors[0] is None
        assert neighbors[1] is None


class TestSyllable:
    @pytest.fixture
    def syllables(self):
        return [
            Syllable("/ba/"),
            Syllable("/bab/"),
            Syllable("/boa/"),
            Syllable("/boab/"),
            Syllable("/ab/"),
            Syllable("/b/"),
        ]

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

    def test_nucleus_index(self, syllables):
        assert syllables[0].nucleus_index == (1, 1)
        assert syllables[1].nucleus_index == (1, 1)
        assert syllables[2].nucleus_index == (1, 2)
        assert syllables[3].nucleus_index == (1, 2)
        assert syllables[4].nucleus_index == (0, 0)
        assert syllables[5].nucleus_index is None

    def test_nucleus(self, syllables):
        assert syllables[0].nucleus == "a"
        assert syllables[1].nucleus == "a"
        assert syllables[2].nucleus == "oa"
        assert syllables[3].nucleus == "oa"
        assert syllables[4].nucleus == "a"
        assert syllables[5].nucleus is None

    def test_onset(self, syllables):
        assert syllables[0].onset == "b"
        assert syllables[1].onset == "b"
        assert syllables[2].onset == "b"
        assert syllables[3].onset == "b"
        assert syllables[4].onset is None
        assert syllables[5].onset is None

    def test_coda(self, syllables):
        assert syllables[0].coda is None
        assert syllables[1].coda == "b"
        assert syllables[2].coda is None
        assert syllables[3].coda == "b"
        assert syllables[4].coda == "b"
        assert syllables[5].coda is None
