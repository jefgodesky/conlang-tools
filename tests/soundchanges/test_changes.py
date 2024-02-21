from typing import List
import pytest
from language.classes import Phonology, Phonotactics, Language
from phonemes.consonants import Consonant
from phonemes.roots import Root
from phonemes.vowels import Vowel, get_vowel
from soundchanges.changes import (
    change,
    apply_change,
    describe_vowel_change,
    get_affected_syllables,
    devoicing,
    erosion_coda_stops_followed_by_consonant,
    erosion_h_between_vowels,
    erosion_ui_becomes_jw_vowel_pair,
    erosion_voiceless_obstruents,
    erosion_word_final_voiced_consonants,
    erosion_word_final_diphthongs,
    erosion_word_final_short_vowels,
    erosion_word_final_shortening,
    labial_assimilation,
    nasal_assimilation,
    velar_assimilation,
    voicing,
    voicing_assimilation,
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


class TestApplyChange:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1}, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ba/"])

    def test_apply_change(self, example_language):
        def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
            return phoneme.symbol == "a"

        def transformer(phoneme: Consonant | Vowel) -> List[Consonant | Vowel]:
            return [get_vowel("a:")]

        new_words = apply_change(example_language, evaluator, transformer)
        assert new_words[0] == "/ba:/"


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


class TestErosionCodaStopsFollwedByConsonant:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1}, coda={"b": 1})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈbab.ba/", "/ˈbab.ab/", "/bab/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_coda_stops_followed_by_consonants(self, example_language):
        description, words = erosion_coda_stops_followed_by_consonant(example_language)
        expected_description = (
            "**Phonetic Erosion:** Coda stops were dropped when they were followed "
            "by a consonant."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈbab.ab/"
        assert words[2] == "/bab/"


class TestErosionHBetweenVowels:
    @pytest.fixture
    def example_language(self):
        consonants = {"b": 1, "h": 1}
        pt = Phonotactics(onset=consonants, nucleus={"a": 1}, coda=consonants)
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈha.ba/", "/ˈba.ha/", "/ba/", "/ha/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_h_between_vowels(self, example_language):
        description, words = erosion_h_between_vowels(example_language)
        expected_description = "**Phonetic Erosion:** /h/ was dropped between vowels."
        assert description == expected_description
        assert words[0] == "/ˈha.ba/"
        assert words[1] == "/ˈba.a/"
        assert words[2] == "/ba/"
        assert words[3] == "/ha/"


class TestErosionIUBecomesJWVowelPair:
    @pytest.fixture
    def example_language(self):
        nucleus = {"a": 1, "i": 1, "u": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={})
        pl = Phonology(stress="initial", openness=1)
        words = [
            "/ˈbu.bi/",
            "/ˈbia.bi/",
            "/ˈbua.bu/",
            "/ba/",
            "/bia/",
            "/bua/",
            "/bi/",
            "/bu/",
        ]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_ui_becomes_jw_vowel_pair(self, example_language):
        description, words = erosion_ui_becomes_jw_vowel_pair(example_language)
        expected_description = (
            "**Phonetic Erosion:** /i/ became /j/ and /u/ became /w/ "
            "when followed by another vowel."
        )
        assert description == expected_description
        assert words[0] == "/ˈbu.bi/"
        assert words[1] == "/ˈbja.bi/"
        assert words[2] == "/ˈbwa.bu/"
        assert words[3] == "/ba/"
        assert words[4] == "/bja/"
        assert words[5] == "/bwa/"
        assert words[6] == "/bi/"
        assert words[7] == "/bu/"


class TestErosionVoicelessObstruents:
    @pytest.fixture
    def example_language(self):
        consonants = {"b": 1, "p": 1, "m̥": 1}
        pt = Phonotactics(onset=consonants, nucleus={"a": 1}, coda=consonants)
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.pat/", "/pat/", "/ˈba.bat/", "/ˈba.m̥at/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_voiceless_obstruents(self, example_language):
        description, words = erosion_voiceless_obstruents(example_language)
        expected_description = (
            "**Phonetic Erosion:** Vowels were dropped "
            "between voiceless obstruents in unstressed "
            "syllables."
        )
        assert description == expected_description
        assert words[0] == "/bapt/"
        assert words[1] == "/pat/"
        assert words[2] == "/ˈba.bat/"
        assert words[3] == "/ˈba.m̥at/"


class TestErosionWordFinalDiphthongs:
    @pytest.fixture
    def example_language(self):
        nucleus = {"a": 1, "a:": 1, "ao": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={"b": 1})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/ˈba.bao/", "/ba/", "/bao/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_word_final_diphthongs(self, example_language):
        description, words = erosion_word_final_diphthongs(example_language)
        expected_description = (
            "**Phonetic Erosion:** Diphthongs that occurred at the end of "
            "a word were simplified into the long-vowel form of the first "
            "vowel in the original diphthong."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈba.ba:/"
        assert words[2] == "/ba/"
        assert words[3] == "/ba:/"


class TestErosionWordFinalShortVowels:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1}, coda={"b": 1})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/ba/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_word_final_short_vowels(self, example_language):
        description, words = erosion_word_final_short_vowels(example_language)
        expected_description = (
            "**Phonetic Erosion:** Short vowels that occurred as the last "
            "sound in a word were dropped."
        )
        assert description == expected_description
        assert words[0] == "/bab/"
        assert words[1] == "/b/"


class TestErosionWordFinalShortening:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "a:": 1}, coda={"b": 1})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba:.ba/", "/ˈba.ba:/", "/ba:/", "/ba/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_word_final_short_vowels(self, example_language):
        description, words = erosion_word_final_shortening(example_language)
        expected_description = (
            "**Phonetic Erosion:** Long vowels that occurred as the last "
            "sound in a word became short vowels."
        )
        assert description == expected_description
        assert words[0] == "/ˈba:.ba/"
        assert words[1] == "/ˈba.ba/"
        assert words[2] == "/ba/"
        assert words[3] == "/ba/"


class TestErosionWordFinalVoicedConsonants:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1}, coda={"b": 1, "p": 1})
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.bab/", "/bap/", "/bab/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_erosion_word_final_voiced_consonants(self, example_language):
        description, words = erosion_word_final_voiced_consonants(example_language)
        expected_description = (
            "**Phonetic Erosion:** Voiced consonants at the end of words "
            "became voiceless."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.bap/"
        assert words[1] == "/bap/"
        assert words[2] == "/bap/"


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


class TestLabialAssimilation:
    @pytest.fixture
    def example_language(self):
        consonants = {"b": 1, "p": 1, "m": 1, "t": 1}
        pt = Phonotactics(onset=consonants, nucleus={"a": 1}, coda=consonants)
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/ˈbamt.ab/", "/ba/", "/mabt/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_labial_assimilation(self, example_language):
        description, words = labial_assimilation(example_language)
        expected_description = (
            "**Labial Assimilation:** Non-labial consonants became labial "
            "consonants when they occurred next to labial consonants."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈbamp.ab/"
        assert words[2] == "/ba/"
        assert words[3] == "/mabp/"


class TestNasalAssimilation:
    @pytest.fixture
    def example_language(self):
        consonants = {"b": 1, "m": 1, "n": 1, "d": 1, "k": 1}
        pt = Phonotactics(onset=consonants, nucleus={"a": 1}, coda=consonants)
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈbna.da/", "/amd/", "/amk/", "/ba/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_nasal_assimilation(self, example_language):
        description, words = nasal_assimilation(example_language)
        expected_description = (
            "**Nasal Assimilation:** Non-nasal consonants became nasal "
            "consonants when they occurred next to nasal consonants."
        )
        assert description == expected_description
        assert words[0] == "/ˈmna.da/"
        assert words[1] == "/amn/"
        assert words[2] == "/amk/"
        assert words[3] == "/ba/"


class TestVelarAssimilation:
    @pytest.fixture
    def example_language(self):
        consonants = {"k": 1, "g": 1, "b": 1, "p": 1, "w": 1}
        pt = Phonotactics(onset=consonants, nucleus={"a": 1}, coda=consonants)
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/ˈbabk.ab/", "/ba/", "/babk/", "/bawk/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_velar_assimilation(self, example_language):
        description, words = velar_assimilation(example_language)
        expected_description = (
            "**Velar Assimilation:** Non-velar consonants became velar "
            "consonants when they occurred next to velar consonants."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈbagk.ab/"
        assert words[2] == "/ba/"
        assert words[3] == "/bagk/"
        assert words[4] == "/bawk/"


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
            "**Voicing:** Unvoiced consonants became voiced between vowels."
        )
        assert description == expected_description
        assert words[0] == "/ˈpa.ba/"


class TestVoicingAssimilation:
    @pytest.fixture
    def example_language(self):
        consonants = {"p": 1, "b": 1, "t": 1, "d": 1, "k": 1}
        pt = Phonotactics(onset=consonants, nucleus={"a": 1}, coda=consonants)
        pl = Phonology(stress="initial", openness=1)
        words = ["/ˈba.ba/", "/ˈbapd.ab/", "/ba/", "/bapd/", "/babt/", "/bakd/"]
        return Language(phonotactics=pt, phonology=pl, words=words)

    def test_voicing_assimilation(self, example_language):
        description, words = voicing_assimilation(example_language)
        expected_description = (
            "**Voicing Assimilation:** Voiceless consonants became voiced "
            "when they occurred next to voiced consonants."
        )
        assert description == expected_description
        assert words[0] == "/ˈba.ba/"
        assert words[1] == "/ˈbabd.ab/"
        assert words[2] == "/ba/"
        assert words[3] == "/babd/"
        assert words[4] == "/babd/"
        assert words[5] == "/bakd/"


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
