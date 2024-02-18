import pytest
from language.classes import Phonology, Phonotactics, Stress


class TestPhonology:
    def test_creates_phonology(self):
        phones = Phonology()
        assert isinstance(phones, Phonology)

    def test_defaults_stress_to_initial(self):
        phones = Phonology()
        assert phones.stress == "initial"

    def test_can_set_stress_initial(self):
        phones = Phonology(stress="initial")
        assert phones.stress == "initial"

    def test_can_set_stress_final(self):
        phones = Phonology(stress="final")
        assert phones.stress == "final"

    def test_can_set_stress_penultimate(self):
        phones = Phonology(stress="penultimate")
        assert phones.stress == "penultimate"

    def test_can_set_stress_antepenultimate(self):
        phones = Phonology(stress="antepenultimate")
        assert phones.stress == "antepenultimate"

    def test_can_set_stress_heavy(self):
        phones = Phonology(stress="heavy")
        assert phones.stress == "heavy"

    def test_can_set_stress_random(self):
        phones = Phonology(stress="random")
        assert phones.stress == "random"

    def test_cannot_set_stress_other(self):
        with pytest.raises(TypeError):
            Phonology(stress="other")

    def test_defaults_openness_50(self):
        phones = Phonology()
        assert phones.openness == 0.5

    def test_can_set_openness(self):
        phones = Phonology(openness=0.75)
        assert phones.openness == 0.75


class TestPhonotactics:
    def test_creates_phonotactics(self):
        phones = Phonotactics()
        assert isinstance(phones, Phonotactics)

    def test_initializes_empty_onset(self):
        phones = Phonotactics()
        assert str(phones.onset) == "{}"

    def test_can_set_onset(self):
        phones = Phonotactics(onset={"a": 1})
        assert phones.onset["a"] == 1

    def test_initializes_empty_nucleus(self):
        phones = Phonotactics()
        assert str(phones.nucleus) == "{}"

    def test_can_set_nucleus(self):
        phones = Phonotactics(nucleus={"a": 1})
        assert phones.nucleus["a"] == 1

    def test_initializes_empty_coda(self):
        phones = Phonotactics()
        assert str(phones.coda) == "{}"

    def test_can_set_coda(self):
        phones = Phonotactics(coda={"a": 1})
        assert phones.coda["a"] == 1


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
