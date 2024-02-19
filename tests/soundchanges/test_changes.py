import pytest
from language.classes import Phonology, Phonotactics, Language
from soundchanges.changes import (
    change,
    vowel_backing,
    vowel_fronting,
    vowel_lowering,
    vowel_raising,
)


class TestVowelBacking:
    @pytest.fixture
    def example_language(self):
        nucleus = {"a": 1, "ɑ": 1, "i": 1, "u": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ˈba.ba/", "/ˈbɑ.ba/"])

    def test_vowel_backing(self, example_language):
        description, words = vowel_backing(example_language, syllables="all")
        exdesc_title = "**Vowel Backing:** "
        exdesc_changes = "/a/ became /ɑ/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbɑ.bɑ/"
        assert words[1] == "/ˈbɑ.bɑ/"

    def test_vowel_backing_stressed(self, example_language):
        description, words = vowel_backing(example_language, syllables="stressed")
        exdesc_title = "**Vowel Backing:** "
        exdesc_changes = "/a/ became /ɑ/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbɑ.ba/"
        assert words[1] == "/ˈbɑ.ba/"

    def test_vowel_backing_randomized(self, example_language):
        description, _ = vowel_backing(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelFronting:
    @pytest.fixture
    def example_language(self):
        nucleus = {"a": 1, "ɑ": 1, "i": 1, "u": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ˈbɑ.bɑ/", "/ˈba.ba/"])

    def test_vowel_fronting(self, example_language):
        description, words = vowel_fronting(example_language, syllables="all")
        exdesc_title = "**Vowel Fronting:** "
        exdesc_changes = "/ɑ/ became /a/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈba.ba/"

    def test_vowel_fronting_stressed(self, example_language):
        description, words = vowel_fronting(example_language, syllables="stressed")
        exdesc_title = "**Vowel Fronting:** "
        exdesc_changes = "/ɑ/ became /a/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.bɑ/"
        assert words[1] == "/ˈba.ba/"

    def test_vowel_fronting_randomized(self, example_language):
        description, _ = vowel_fronting(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelLowering:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "e": 1, "i": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ˈba.be/", "/ˈbe.bi/"])

    def test_vowel_lowering(self, example_language):
        description, words = vowel_lowering(example_language, syllables="all")
        exdesc_title = "**Vowel Lowering:** "
        exdesc_changes = "/i/ became /e/ and /e/ became /a/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈba.be/"

    def test_vowel_lowering_stressed(self, example_language):
        description, words = vowel_lowering(example_language, syllables="stressed")
        exdesc_title = "**Vowel Lowering:** "
        exdesc_changes = "/i/ became /e/ and /e/ became /a/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.be/"
        assert words[1] == "/ˈba.bi/"

    def test_vowel_lowering_randomized(self, example_language):
        description, _ = vowel_lowering(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelRaising:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "e": 1, "i": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ˈba.be/", "/ˈbe.bi/"])

    def test_vowel_raising(self, example_language):
        description, words = vowel_raising(example_language, syllables="all")
        exdesc_title = "**Vowel Raising:** "
        exdesc_changes = "/a/ became /e/ and /e/ became /i/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbe.bi/"
        assert words[1] == "/ˈbi.bi/"

    def test_vowel_raising_stressed(self, example_language):
        description, words = vowel_raising(example_language, syllables="stressed")
        exdesc_title = "**Vowel Raising:** "
        exdesc_changes = "/a/ became /e/ and /e/ became /i/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbe.be/"
        assert words[1] == "/ˈbi.bi/"

    def test_vowel_raising_randomized(self, example_language):
        description, _ = vowel_raising(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestChange:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ba/"])

    def test_change(self, example_language):
        description, words = change(example_language)
        assert isinstance(description, str)
        assert all(isinstance(word, str) for word in words)
        assert len(words) == len(example_language.words)
