import pytest
from language.classes import Phonology, Phonotactics, Language
from soundchanges.vowel_raise import vowel_raise


class TestVowelRaise:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "e": 1, "i": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ˈba.be/", "/ˈbe.bi/"])

    def test_vowel_raise(self, example_language):
        description, words = vowel_raise(example_language, syllables="all")
        exdesc_title = "**Vowel Raise:** "
        exdesc_changes = "/a/ became /e/ and /e/ became /i/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbe.bi/"
        assert words[1] == "/ˈbi.bi/"

    def test_vowel_raise_stressed(self, example_language):
        description, words = vowel_raise(example_language, syllables="stressed")
        exdesc_title = "**Vowel Raise:** "
        exdesc_changes = "/a/ became /e/ and /e/ became /i/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbe.be/"
        assert words[1] == "/ˈbi.bi/"

    def test_vowel_raise_randomized(self, example_language):
        description, _ = vowel_raise(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables
