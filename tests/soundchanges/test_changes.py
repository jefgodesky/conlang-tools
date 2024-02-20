import pytest
from language.classes import Phonology, Phonotactics, Language
from soundchanges.changes import (
    change,
    describe_vowel_change,
    get_affected_syllables,
    vowel_backing,
    vowel_fronting,
    vowel_lengthening,
    vowel_lowering,
    vowel_raising,
    vowel_shortening,
    vowel_splitting_palatalization,
)


class TestDescribeVowelChange:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "e": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ba/"])

    def test_all(self, example_language):
        mapping = example_language.vowel_mapping("height")
        description, affected, affected_keys = describe_vowel_change(
            mapping, "Lowering", "all"
        )
        assert description == "**Vowel Lowering:** /a/ became /e/ in all syllables."
        assert affected == "all"
        assert len(affected_keys) == 1
        assert affected_keys[0] == "a"

    def test_stressed(self, example_language):
        mapping = example_language.vowel_mapping("height")
        description, affected, affected_keys = describe_vowel_change(
            mapping, "Lowering", "stressed"
        )
        assert (
            description == "**Vowel Lowering:** /a/ became /e/ in stressed syllables."
        )
        assert affected == "stressed"
        assert len(affected_keys) == 1
        assert affected_keys[0] == "a"

    def test_random(self, example_language):
        mapping = example_language.vowel_mapping("height")
        description, affected, _ = describe_vowel_change(mapping, "Lowering")
        is_all = "all syllables" in description
        is_stressed = "stressed syllables" in description
        assert is_all or is_stressed
        assert affected in ["all", "stressed"]


class TestGetAffectedSyllables:
    def test_all(self):
        assert get_affected_syllables("all") == "all"

    def test_stressed(self):
        assert get_affected_syllables("stressed") == "stressed"

    def test_random(self):
        assert get_affected_syllables() in ["all", "stressed"]


class TestVowelBacking:
    @pytest.fixture
    def example_language(self):
        nucleus = {"a": 1, "ɑ": 1, "i": 1, "u": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/ˈbɑ.ba/", "/ba/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_backing(self, example_language):
        description, words = vowel_backing(example_language, syllables="all")
        exdesc_title = "**Vowel Backing:** "
        exdesc_changes = "/a/ became /ɑ/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbɑ.bɑ/"
        assert words[1] == "/ˈbɑ.bɑ/"
        assert words[2] == "/bɑ/"

    def test_vowel_backing_stressed(self, example_language):
        description, words = vowel_backing(example_language, syllables="stressed")
        exdesc_title = "**Vowel Backing:** "
        exdesc_changes = "/a/ became /ɑ/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbɑ.ba/"
        assert words[1] == "/ˈbɑ.ba/"
        assert words[2] == "/bɑ/"

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
        words = ["/ˈbɑ.bɑ/", "/ˈba.ba/", "/bɑ/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_fronting(self, example_language):
        description, words = vowel_fronting(example_language, syllables="all")
        exdesc_title = "**Vowel Fronting:** "
        exdesc_changes = "/ɑ/ became /a/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈba.ba/"
        assert words[2] == "/ba/"

    def test_vowel_fronting_stressed(self, example_language):
        description, words = vowel_fronting(example_language, syllables="stressed")
        exdesc_title = "**Vowel Fronting:** "
        exdesc_changes = "/ɑ/ became /a/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.bɑ/"
        assert words[1] == "/ˈba.ba/"
        assert words[2] == "/ba/"

    def test_vowel_fronting_randomized(self, example_language):
        description, _ = vowel_fronting(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelLengthening:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a:": 1, "a": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/ba/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_lengthening(self, example_language):
        description, words = vowel_lengthening(example_language, syllables="all")
        exdesc_title = "**Vowel Lengthening:** "
        exdesc_changes = "/a/ became /a:/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba:.ba:/"
        assert words[1] == "/ba:/"

    def test_vowel_lengthening_stressed(self, example_language):
        description, words = vowel_lengthening(example_language, syllables="stressed")
        exdesc_title = "**Vowel Lengthening:** "
        exdesc_changes = "/a/ became /a:/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba:.ba/"
        assert words[1] == "/ba:/"

    def test_vowel_lengthening_randomized(self, example_language):
        description, _ = vowel_lengthening(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelLowering:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "e": 1, "i": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.be/", "/ˈbe.bi/", "/be/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_lowering(self, example_language):
        description, words = vowel_lowering(example_language, syllables="all")
        exdesc_title = "**Vowel Lowering:** "
        exdesc_changes = "/i/ became /e/ and /e/ became /a/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈba.be/"
        assert words[2] == "/ba/"

    def test_vowel_lowering_stressed(self, example_language):
        description, words = vowel_lowering(example_language, syllables="stressed")
        exdesc_title = "**Vowel Lowering:** "
        exdesc_changes = "/i/ became /e/ and /e/ became /a/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.be/"
        assert words[1] == "/ˈba.bi/"
        assert words[2] == "/ba/"

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
        words = ["/ˈba.be/", "/ˈbe.bi/", "/be/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_raising(self, example_language):
        description, words = vowel_raising(example_language, syllables="all")
        exdesc_title = "**Vowel Raising:** "
        exdesc_changes = "/a/ became /e/ and /e/ became /i/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbe.bi/"
        assert words[1] == "/ˈbi.bi/"
        assert words[2] == "/bi/"

    def test_vowel_raising_stressed(self, example_language):
        description, words = vowel_raising(example_language, syllables="stressed")
        exdesc_title = "**Vowel Raising:** "
        exdesc_changes = "/a/ became /e/ and /e/ became /i/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈbe.be/"
        assert words[1] == "/ˈbi.bi/"
        assert words[2] == "/bi/"

    def test_vowel_raising_randomized(self, example_language):
        description, _ = vowel_raising(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelShortening:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a:": 1, "a": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba:.ba:/", "/ba:/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_shortening(self, example_language):
        description, words = vowel_shortening(example_language, syllables="all")
        exdesc_title = "**Vowel Shortening:** "
        exdesc_changes = "/a:/ became /a/"
        exdesc_syllables = " in all syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ba/"

    def test_vowel_shortening_stressed(self, example_language):
        description, words = vowel_shortening(example_language, syllables="stressed")
        exdesc_title = "**Vowel Shortening:** "
        exdesc_changes = "/a:/ became /a/"
        exdesc_syllables = " in stressed syllables."
        expected_desc = exdesc_title + exdesc_changes + exdesc_syllables
        assert description == expected_desc
        assert words[0] == "/ˈba.ba:/"
        assert words[1] == "/ba/"

    def test_vowel_shortening_randomized(self, example_language):
        description, _ = vowel_shortening(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelSplittingPalatalization:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a:": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/baʧ/", "/baʃ/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_splitting_palatalization(self, example_language):
        description, words = vowel_splitting_palatalization(example_language)
        exdesc_title = "**Vowel Splitting:** "
        exdesc_changes = "/a/ became /æ/ when followed by a palatal consonant."
        expected_desc = exdesc_title + exdesc_changes
        assert description == expected_desc
        assert words[0] == "/bæʧ/"
        assert words[1] == "/baʃ/"


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
