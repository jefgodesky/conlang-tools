import pytest
from language.classes import Language, Phonology, Phonotactics, Stress


class TestLanguage:
    def test_creates_language(self):
        lang = Language()
        assert isinstance(lang, Language)

    def test_has_phonotactics(self):
        lang = Language()
        assert isinstance(lang.phonotactics, Phonotactics)

    def test_can_take_phonotactics(self):
        tactics = Phonotactics(onset={"a": 1})
        lang = Language(phonotactics=tactics)
        assert lang.phonotactics.onset["a"] == 1

    def test_has_phonology(self):
        lang = Language()
        assert isinstance(lang.phonology, Phonology)

    def test_can_take_phonology(self):
        phones = Phonology(stress="antepenultimate")
        lang = Language(phonology=phones)
        assert lang.phonology.stress == "antepenultimate"

    def test_has_words(self):
        lang = Language()
        assert len(lang.words) == 0

    def test_can_take_words(self):
        lang = Language(words=["/ba/"])
        assert len(lang.words) == 1
        assert lang.words[0] == "/ba/"

    def test_load(self):
        lang = Language.load("example")
        assert isinstance(lang, Language)
        assert lang.phonotactics.onset["b"] == 1
        assert lang.phonology.stress == "initial"
        assert "/ba/" in lang.words

    def test_load_fail(self):
        with pytest.raises(FileNotFoundError):
            Language.load("thislanguagedoesnotexist")


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

    def test_build_choices(self):
        phones = Phonotactics(onset={"b": 2, "c": 1})
        assert ", ".join(phones.choices("onset")) == "b, b, c"

    def test_build_choices_defaults_to_nucleus(self):
        phones = Phonotactics(nucleus={"a": 2, "e": 1})
        assert ", ".join(phones.choices()) == "a, a, e"

    def test_build_choices_other_to_nucleus(self):
        phones = Phonotactics(nucleus={"a": 2, "e": 1})
        assert ", ".join(phones.choices("other")) == "a, a, e"


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
