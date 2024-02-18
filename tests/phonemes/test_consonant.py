import pytest
from phonemes.consonants import ConsonantPlace


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
