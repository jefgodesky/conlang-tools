import pytest
from language.classes import Stress


class TestStress:
    def test_creates_stress(self):
        stress = Stress()
        assert isinstance(stress, Stress)

    def test_defaults_initial(self):
        stress = Stress()
        print(stress)
        assert stress == "initial"

    def test_can_set_initial(self):
        stress = Stress("initial")
        assert stress == "initial"

    def test_can_set_final(self):
        stress = Stress("final")
        assert stress == "final"

    def test_can_set_penultimate(self):
        stress = Stress("penultimate")
        assert stress == "penultimate"

    def test_can_set_antepenultimate(self):
        stress = Stress("antepenultimate")
        assert stress == "antepenultimate"

    def test_can_set_heavy(self):
        stress = Stress("heavy")
        assert stress == "heavy"

    def test_can_set_random(self):
        stress = Stress("random")
        assert stress == "random"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            stress = Stress("other")
            assert stress != "other"

    def test_returns_types(self):
        expected = "initial, final, penultimate, antepenultimate, heavy, random"
        assert ", ".join(Stress.types()) == expected

    def test_isstress_initial_true(self):
        assert Stress.isstress("initial") is True

    def test_isstress_final_true(self):
        assert Stress.isstress("final") is True

    def test_isstress_penultimate_true(self):
        assert Stress.isstress("penultimate") is True

    def test_isstress_antepenultimate_true(self):
        assert Stress.isstress("antepenultimate") is True

    def test_isstress_heavy_true(self):
        assert Stress.isstress("heavy") is True

    def test_isstress_random_true(self):
        assert Stress.isstress("random") is True

    def test_isstress_other_false(self):
        assert Stress.isstress("other") is False
