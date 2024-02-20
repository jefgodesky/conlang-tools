import pytest
from language.classes import Phonology, Phonotactics, Language
from soundchanges.changes import (
    change,
    describe_vowel_change,
    get_affected_syllables,
    devoicing,
    voicing,
    vowel_backing,
    vowel_fronting,
    vowel_lengthening,
    vowel_lowering,
    vowel_raising,
    vowel_shortening,
    vowel_splitting,
    vowel_splitting_palatalization,
    vowel_splitting_stress_diphthongization,
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


class TestDevoicing:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1}, coda={"b": 1, "bt": 1})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/bab/", "/babt/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_devoicing(self, example_language):
        description, words = devoicing(example_language)
        expected_description = (
            "**Devoicing:** Voiced consonants became voiceless "
            "at the end of words or next to voiceless consonants."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/bap/"
        assert words[2] == "/bapt/"


class TestVoicing:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1, "p": 1}, nucleus={"a": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈpa.pa/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_voicing(self, example_language):
        description, words = voicing(example_language)
        expected_description = (
            "**Voicing:** Unvoiced consonants became voiced " "between vowels."
        )
        assert description == expected_description
        assert words[0] == "/ˈpa.ba/"


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
        expected_description = "**Vowel Backing:** /a/ became /ɑ/ in all syllables."
        assert description == expected_description
        assert words[0] == "/ˈbɑ.bɑ/"
        assert words[1] == "/ˈbɑ.bɑ/"
        assert words[2] == "/bɑ/"

    def test_vowel_backing_stressed(self, example_language):
        description, words = vowel_backing(example_language, syllables="stressed")
        expected_description = (
            "**Vowel Backing:** /a/ became /ɑ/ in stressed syllables."
        )
        assert description == expected_description
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
        expected_description = "**Vowel Fronting:** /ɑ/ became /a/ in all syllables."
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈba.ba/"
        assert words[2] == "/ba/"

    def test_vowel_fronting_stressed(self, example_language):
        description, words = vowel_fronting(example_language, syllables="stressed")
        expected_description = (
            "**Vowel Fronting:** /ɑ/ became /a/ in stressed syllables."
        )
        assert description == expected_description
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
        expected_description = (
            "**Vowel Lengthening:** /a/ became /a:/ in all syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈba:.ba:/"
        assert words[1] == "/ba:/"

    def test_vowel_lengthening_stressed(self, example_language):
        description, words = vowel_lengthening(example_language, syllables="stressed")
        expected_description = (
            "**Vowel Lengthening:** /a/ became /a:/ in stressed syllables."
        )
        assert description == expected_description
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
        expected_description = (
            "**Vowel Lowering:** /i/ became /e/ and /e/ became /a/ in all syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈba.be/"
        assert words[2] == "/ba/"

    def test_vowel_lowering_stressed(self, example_language):
        description, words = vowel_lowering(example_language, syllables="stressed")
        expected_description = "**Vowel Lowering:** /i/ became /e/ and /e/ became /a/ in stressed syllables."
        assert description == expected_description
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
        expected_description = (
            "**Vowel Raising:** /a/ became /e/ and /e/ became /i/ in all syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈbe.bi/"
        assert words[1] == "/ˈbi.bi/"
        assert words[2] == "/bi/"

    def test_vowel_raising_stressed(self, example_language):
        description, words = vowel_raising(example_language, syllables="stressed")
        expected_description = "**Vowel Raising:** /a/ became /e/ and /e/ became /i/ in stressed syllables."
        assert description == expected_description
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
        expected_description = "**Vowel Shortening:** /a:/ became /a/ in all syllables."
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ba/"

    def test_vowel_shortening_stressed(self, example_language):
        description, words = vowel_shortening(example_language, syllables="stressed")
        expected_description = (
            "**Vowel Shortening:** /a:/ became /a/ in stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba:/"
        assert words[1] == "/ba/"

    def test_vowel_shortening_randomized(self, example_language):
        description, _ = vowel_shortening(example_language)
        stressed_syllables = "stressed syllables" in description
        all_syllables = "all syllables" in description
        assert stressed_syllables or all_syllables


class TestVowelSplitting:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a:": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/baʧ/", "/baʃ/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_splitting(self, example_language):
        description, _ = vowel_splitting(example_language)
        assert "Vowel Splitting" in description


class TestVowelSplittingPalatalization:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a:": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/baʧ/", "/baʃ/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_vowel_splitting_palatalization(self, example_language):
        description, words = vowel_splitting_palatalization(example_language)
        expected_description = (
            "**Vowel Splitting:** /a/ became /æ/ when followed by "
            "a palatal consonant."
        )
        assert description == expected_description
        assert words[0] == "/bæʧ/"
        assert words[1] == "/baʃ/"


class TestVowelSplittingStressDiphthongization:
    @pytest.fixture
    def example_language(self):
        nucleus = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈban.pan/", "/ˈben.pen/", "/ˈbin.pin/", "/ˈbon.pon/", "/ˈbun.pun/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    @pytest.fixture
    def fn(self):
        return vowel_splitting_stress_diphthongization

    def test_vowel_splitting_stress_diphthongization_a_au(self, example_language, fn):
        description, words = fn(example_language, "a", "au")
        expected_description = (
            "**Vowel Splitting:** /a/ became /au/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈbaun.pan/"
        assert words[1] == "/ˈben.pen/"
        assert words[2] == "/ˈbin.pin/"
        assert words[3] == "/ˈbon.pon/"
        assert words[4] == "/ˈbun.pun/"

    def test_vowel_splitting_stress_diphthongization_a_ai(self, example_language, fn):
        description, words = fn(example_language, "a", "ai")
        expected_description = (
            "**Vowel Splitting:** /a/ became /ai/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈbain.pan/"
        assert words[1] == "/ˈben.pen/"
        assert words[2] == "/ˈbin.pin/"
        assert words[3] == "/ˈbon.pon/"
        assert words[4] == "/ˈbun.pun/"

    def test_vowel_splitting_stress_diphthongization_e_ei(self, example_language, fn):
        description, words = fn(example_language, "e", "ei")
        expected_description = (
            "**Vowel Splitting:** /e/ became /ei/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈban.pan/"
        assert words[1] == "/ˈbein.pen/"
        assert words[2] == "/ˈbin.pin/"
        assert words[3] == "/ˈbon.pon/"
        assert words[4] == "/ˈbun.pun/"

    def test_vowel_splitting_stress_diphthongization_i_ie(self, example_language, fn):
        description, words = fn(example_language, "i", "ie")
        expected_description = (
            "**Vowel Splitting:** /i/ became /ie/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈban.pan/"
        assert words[1] == "/ˈben.pen/"
        assert words[2] == "/ˈbien.pin/"
        assert words[3] == "/ˈbon.pon/"
        assert words[4] == "/ˈbun.pun/"

    def test_vowel_splitting_stress_diphthongization_i_ia(self, example_language, fn):
        description, words = fn(example_language, "i", "ia")
        expected_description = (
            "**Vowel Splitting:** /i/ became /ia/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈban.pan/"
        assert words[1] == "/ˈben.pen/"
        assert words[2] == "/ˈbian.pin/"
        assert words[3] == "/ˈbon.pon/"
        assert words[4] == "/ˈbun.pun/"

    def test_vowel_splitting_stress_diphthongization_o_oi(self, example_language, fn):
        description, words = fn(example_language, "o", "ou")
        expected_description = (
            "**Vowel Splitting:** /o/ became /ou/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈban.pan/"
        assert words[1] == "/ˈben.pen/"
        assert words[2] == "/ˈbin.pin/"
        assert words[3] == "/ˈboun.pon/"
        assert words[4] == "/ˈbun.pun/"

    def test_vowel_splitting_stress_diphthongization_u_ue(self, example_language, fn):
        description, words = fn(example_language, "u", "ue")
        expected_description = (
            "**Vowel Splitting:** /u/ became /ue/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈban.pan/"
        assert words[1] == "/ˈben.pen/"
        assert words[2] == "/ˈbin.pin/"
        assert words[3] == "/ˈbon.pon/"
        assert words[4] == "/ˈbuen.pun/"

    def test_vowel_splitting_stress_diphthongization_u_uo(self, example_language, fn):
        description, words = fn(example_language, "u", "uo")
        expected_description = (
            "**Vowel Splitting:** /u/ became /uo/ in " "stressed syllables."
        )
        assert description == expected_description
        assert words[0] == "/ˈban.pan/"
        assert words[1] == "/ˈben.pen/"
        assert words[2] == "/ˈbin.pin/"
        assert words[3] == "/ˈbon.pon/"
        assert words[4] == "/ˈbuon.pun/"


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
