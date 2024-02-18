import pytest
from phonemes.consonants import Consonant, ConsonantManner, ConsonantPlace, get_consonants


class TestGetConsonants:
    def test_get_vowels(self):
        consonants = get_consonants()
        assert len(consonants) == 72
        assert all(isinstance(consonant, Consonant) for consonant in consonants)


class TestConsonant:
    def test_creates_consonant(self):
        p = Consonant("p", ConsonantManner("stop"), ConsonantPlace("labial"), False)
        assert isinstance(p, Consonant)
        assert p.symbol == "p"
        assert p.manner == "stop"
        assert isinstance(p.manner, ConsonantManner)
        assert p.place == "labial"
        assert isinstance(p.place, ConsonantPlace)
        assert p.voiced is False
        assert p.category == "obstruent"

    def test_repr(self):
        p = Consonant("p", ConsonantManner("stop"), ConsonantPlace("labial"), False)
        assert str(p) == "[p]"


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

    def test_ismanner_stop_true(self):
        assert ConsonantManner.ismanner("stop") is True

    def test_ismanner_fricative_true(self):
        assert ConsonantManner.ismanner("fricative") is True

    def test_ismanner_affricate_true(self):
        assert ConsonantManner.ismanner("affricate") is True

    def test_ismanner_nasal_true(self):
        assert ConsonantManner.ismanner("nasal") is True

    def test_ismanner_liquid_true(self):
        assert ConsonantManner.ismanner("liquid") is True

    def test_ismanner_other_false(self):
        assert ConsonantManner.ismanner("other") is False

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
        expected = ["labial", "dental", "alveolar-central", "alveolar-lateral",
                    "retroflex", "palatal", "post-alveolar", "velar", "uvular",
                    "pharyngeal", "glottal"]
        assert ", ".join(ConsonantPlace.types()) == ", ".join(expected)

    def test_isplace_labial_true(self):
        assert ConsonantPlace.isplace("labial") is True

    def test_isplace_dental_true(self):
        assert ConsonantPlace.isplace("dental") is True

    def test_isplace_alveolar_central_true(self):
        assert ConsonantPlace.isplace("alveolar-central") is True

    def test_isplace_alveolar_lateral_true(self):
        assert ConsonantPlace.isplace("alveolar-lateral") is True

    def test_isplace_retroflex_true(self):
        assert ConsonantPlace.isplace("retroflex") is True

    def test_isplace_palatal_true(self):
        assert ConsonantPlace.isplace("palatal") is True

    def test_isplace_post_alveolar_true(self):
        assert ConsonantPlace.isplace("post-alveolar") is True

    def test_isplace_velar_true(self):
        assert ConsonantPlace.isplace("velar") is True

    def test_isplace_uvular_true(self):
        assert ConsonantPlace.isplace("uvular") is True

    def test_isplace_pharyngeal_true(self):
        assert ConsonantPlace.isplace("pharyngeal") is True

    def test_isplace_glottal_true(self):
        assert ConsonantPlace.isplace("glottal") is True

    def test_isplace_other_false(self):
        assert ConsonantPlace.isplace("other") is False