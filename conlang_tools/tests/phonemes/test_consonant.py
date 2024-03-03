import pytest
from conlang_tools.phonemes.consonants import (
    Consonant,
    ConsonantManner,
    ConsonantPlace,
)
from conlang_tools.phonemes.collections import get_consonant
from conlang_tools.tests.phonemes.test_collections import TestGetConsonant


class TestConsonant:
    def test_creates_consonant(self):
        p = Consonant("p", ConsonantManner("stop"), ConsonantPlace("labial"), False)
        TestGetConsonant.isp(p)

    def test_repr(self):
        p = Consonant("p", ConsonantManner("stop"), ConsonantPlace("labial"), False)
        assert str(p) == "[p]"

    def test_is_sibilant(self):
        sibilants = ["θ", "ð", "s", "z", "t̪θ", "d̪ð", "Ts", "dz", "ʃ", "ʒ"]
        controls = ["k", "g", "m", "n", "j", "w", "f", "v", "x", "h"]
        sibilant_instances = [get_consonant(symbol) for symbol in sibilants]
        control_instances = [get_consonant(symbol) for symbol in controls]
        assert all([consonant.is_sibilant() for consonant in sibilant_instances])
        assert not any([consonant.is_sibilant() for consonant in control_instances])


class TestConsonantManner:
    def test_creates_consonant_manner(self):
        manner = ConsonantManner()
        assert isinstance(manner, ConsonantManner)

    def test_defaults_stop(self):
        assert ConsonantManner() == "stop"

    def test_can_set_stop(self):
        assert ConsonantManner("stop") == "stop"

    def test_can_set_fricative(self):
        assert ConsonantManner("fricative") == "fricative"

    def test_can_set_affricate(self):
        assert ConsonantManner("affricate") == "affricate"

    def test_can_set_nasal(self):
        assert ConsonantManner("nasal") == "nasal"

    def test_can_set_liquid(self):
        assert ConsonantManner("liquid") == "liquid"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            assert ConsonantManner("other") != "other"

    def test_returns_types(self):
        expected = "stop, fricative, affricate, nasal, liquid"
        assert ", ".join(ConsonantManner.types()) == expected

    def test_is_valid_stop_true(self):
        assert ConsonantManner.is_valid("stop") is True

    def test_is_valid_fricative_true(self):
        assert ConsonantManner.is_valid("fricative") is True

    def test_is_valid_affricate_true(self):
        assert ConsonantManner.is_valid("affricate") is True

    def test_is_valid_nasal_true(self):
        assert ConsonantManner.is_valid("nasal") is True

    def test_is_valid_liquid_true(self):
        assert ConsonantManner.is_valid("liquid") is True

    def test_is_valid_other_false(self):
        assert ConsonantManner.is_valid("other") is False

    def test_stop_is_obstruent(self):
        assert ConsonantManner.category("stop") == "obstruent"

    def test_fricative_is_obstruent(self):
        assert ConsonantManner.category("fricative") == "obstruent"

    def test_affricate_is_obstruent(self):
        assert ConsonantManner.category("affricate") == "obstruent"

    def test_nasal_is_resonant(self):
        assert ConsonantManner.category("nasal") == "resonant"

    def test_liquid_is_resonant(self):
        assert ConsonantManner.category("liquid") == "resonant"

    def test_other_is_na(self):
        assert ConsonantManner.category("other") == "n/a"


class TestConsonantPlace:
    def test_creates_consonant_place(self):
        place = ConsonantPlace()
        assert isinstance(place, ConsonantPlace)

    def test_defaults_labial(self):
        assert ConsonantPlace() == "labial"

    def test_can_set_labial(self):
        assert ConsonantPlace("labial") == "labial"

    def test_can_set_alveolar_central(self):
        assert ConsonantPlace("alveolar-central") == "alveolar-central"

    def test_can_set_alveolar_lateral(self):
        assert ConsonantPlace("alveolar-lateral") == "alveolar-lateral"

    def test_can_set_retroflex(self):
        assert ConsonantPlace("retroflex") == "retroflex"

    def test_can_set_palatal(self):
        assert ConsonantPlace("palatal") == "palatal"

    def test_can_set_post_alveolar(self):
        assert ConsonantPlace("post-alveolar") == "post-alveolar"

    def test_can_set_velar(self):
        assert ConsonantPlace("velar") == "velar"

    def test_can_set_uvular(self):
        assert ConsonantPlace("uvular") == "uvular"

    def test_can_set_pharyngeal(self):
        assert ConsonantPlace("pharyngeal") == "pharyngeal"

    def test_can_set_glottal(self):
        assert ConsonantPlace("glottal") == "glottal"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            assert ConsonantPlace("other") != "other"

    def test_returns_types(self):
        expected = [
            "labial",
            "dental",
            "alveolar-central",
            "alveolar-lateral",
            "retroflex",
            "palatal",
            "post-alveolar",
            "velar",
            "uvular",
            "pharyngeal",
            "glottal",
        ]
        assert ", ".join(ConsonantPlace.types()) == ", ".join(expected)

    def test_is_valid_labial_true(self):
        assert ConsonantPlace.is_valid("labial") is True

    def test_is_valid_dental_true(self):
        assert ConsonantPlace.is_valid("dental") is True

    def test_is_valid_alveolar_central_true(self):
        assert ConsonantPlace.is_valid("alveolar-central") is True

    def test_is_valid_alveolar_lateral_true(self):
        assert ConsonantPlace.is_valid("alveolar-lateral") is True

    def test_is_valid_retroflex_true(self):
        assert ConsonantPlace.is_valid("retroflex") is True

    def test_is_valid_palatal_true(self):
        assert ConsonantPlace.is_valid("palatal") is True

    def test_is_valid_post_alveolar_true(self):
        assert ConsonantPlace.is_valid("post-alveolar") is True

    def test_is_valid_velar_true(self):
        assert ConsonantPlace.is_valid("velar") is True

    def test_is_valid_uvular_true(self):
        assert ConsonantPlace.is_valid("uvular") is True

    def test_is_valid_pharyngeal_true(self):
        assert ConsonantPlace.is_valid("pharyngeal") is True

    def test_is_valid_glottal_true(self):
        assert ConsonantPlace.is_valid("glottal") is True

    def test_is_valid_other_false(self):
        assert ConsonantPlace.is_valid("other") is False
