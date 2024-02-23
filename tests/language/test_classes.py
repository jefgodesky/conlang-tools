import pytest
from language.classes import Language, Phonology, Phonotactics, Stress


class TestLanguage:
    @pytest.fixture
    def example_language(self):
        tactics = Phonotactics(onset={"b": 2}, nucleus={"a": 1}, coda={"c": 1})
        logy = Phonology(stress="initial", openness=0.5)
        words = ["/ba/"]
        return Language(phonotactics=tactics, phonology=logy, words=words)

    @pytest.fixture
    def vowel_change_example(self):
        nucleus = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=[])

    @pytest.fixture
    def vowel_rounded_example(self):
        nucleus = {"a": 1, "ø": 1, "y": 1, "o": 1, "u": 1}
        pt = Phonotactics(onset={"b": 1}, nucleus=nucleus, coda={})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=[])

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

    def test_tracks_generated(self):
        lang = Language()
        assert len(lang.generated) == 0

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

    def test_generate_syllable(self, example_language):
        assert example_language.generate_syllable() in ["ba", "bac"]

    def test_apply_stress_monosyllabic(self):
        lang = Language()
        assert ".".join(lang.apply_stress(["ba"])) == "ba"

    def test_apply_stress_initial(self):
        lang = Language(phonology=Phonology(stress="initial"))
        assert ".".join(lang.apply_stress(["ba", "ba"])) == "ˈba.ba"

    def test_apply_stress_final(self):
        lang = Language(phonology=Phonology(stress="final"))
        assert ".".join(lang.apply_stress(["ba", "ba"])) == "ba.ˈba"

    def test_apply_stress_penultimate3(self):
        lang = Language(phonology=Phonology(stress="penultimate"))
        assert ".".join(lang.apply_stress(["ba", "ba", "ba"])) == "ba.ˈba.ba"

    def test_apply_stress_penultimate2(self):
        lang = Language(phonology=Phonology(stress="penultimate"))
        assert ".".join(lang.apply_stress(["ba", "ba"])) == "ˈba.ba"

    def test_apply_stress_antepenultimate4(self):
        lang = Language(phonology=Phonology(stress="antepenultimate"))
        assert ".".join(lang.apply_stress(["ba", "ba", "ba", "ba"])) == "ba.ˈba.ba.ba"

    def test_apply_stress_antepenultimate3(self):
        lang = Language(phonology=Phonology(stress="antepenultimate"))
        assert ".".join(lang.apply_stress(["ba", "ba", "ba"])) == "ˈba.ba.ba"

    def test_apply_stress_antepenultimate2(self):
        lang = Language(phonology=Phonology(stress="antepenultimate"))
        assert ".".join(lang.apply_stress(["ba", "ba"])) == "ˈba.ba"

    def test_apply_stress_heavy(self):
        lang = Language(phonology=Phonology(stress="heavy"))
        assert ".".join(lang.apply_stress(["ba", "ba:", "ba"])) == "ba.ˈba:.ba"
        assert ".".join(lang.apply_stress(["ba", "bab", "ba"])) == "ba.ˈbab.ba"
        assert ".".join(lang.apply_stress(["ba:", "ba:b", "bab"])) == "ba:.ˈba:b.bab"

    def test_apply_stress_random(self):
        lang = Language(phonology=Phonology(stress="random"))
        possibilities = ["ˈba.ba", "ba.ˈba"]
        assert ".".join(lang.apply_stress(["ba", "ba"])) in possibilities

    def test_generate_monosyllabic_word(self, example_language):
        word = example_language.generate_word()
        possibilities = ["/ba/", "/bac/"]
        assert word in possibilities

    def test_generate_bisyllabic_word(self, example_language):
        word = example_language.generate_word(num_syllables=2)
        possibilities = [
            "/ˈba.ba/",
            "/ˈba.bac/",
            "/ˈbac.ba/",
            "/ˈbac.bac/",
        ]
        assert word in possibilities

    def test_vowel_raise_mapping(self, vowel_change_example):
        mapping = vowel_change_example.vowel_height_mapping()
        assert mapping["a"].symbol == "e"
        assert mapping["e"].symbol == "i"
        assert mapping["i"].symbol == "i"
        assert mapping["o"].symbol == "u"
        assert mapping["u"].symbol == "u"

    def test_vowel_lower_mapping(self, vowel_change_example):
        mapping = vowel_change_example.vowel_height_mapping(rise=False)
        assert mapping["a"].symbol == "a"
        assert mapping["e"].symbol == "a"
        assert mapping["i"].symbol == "e"
        assert mapping["o"].symbol == "o"
        assert mapping["u"].symbol == "o"

    def test_vowel_front_mapping(self, vowel_rounded_example):
        mapping = vowel_rounded_example.vowel_location_mapping()
        assert mapping["a"].symbol == "a"
        assert mapping["ø"].symbol == "ø"
        assert mapping["y"].symbol == "y"
        assert mapping["o"].symbol == "ø"
        assert mapping["u"].symbol == "y"

    def test_vowel_back_mapping(self, vowel_rounded_example):
        mapping = vowel_rounded_example.vowel_location_mapping(fronting=False)
        assert mapping["a"].symbol == "a"
        assert mapping["ø"].symbol == "o"
        assert mapping["y"].symbol == "u"
        assert mapping["o"].symbol == "o"
        assert mapping["u"].symbol == "u"

    def test_generate_new_word(self, example_language):
        word = example_language.generate_new_word()
        assert word not in example_language.words

    def test_generate_new_word_does_not_repeat(self, example_language):
        w1 = example_language.generate_new_word()
        w2 = example_language.generate_new_word()
        assert len(example_language.generated) == 2
        assert w1 != w2

    def test_generate_new_words(self, example_language):
        new_words = example_language.generate_new_words(3)
        assert len(new_words) == 3
        assert len(example_language.generated) == 3

    def test_take_inventory(self):
        tactics = Phonotactics(onset={"bb": 2}, nucleus={"a": 1}, coda={})
        logy = Phonology(stress="initial", openness=1)
        lang = Language(phonotactics=tactics, phonology=logy, words=["/bba/"])
        consonants, vowels = lang.take_inventory()
        assert len(consonants) == 1
        assert consonants[0].symbol == "b"
        assert len(vowels) == 1

    def test_from_words(self):
        words = ["/ba/", "/ˈba.ba/", "/bab/"]
        lang = Language.from_words(words)
        assert isinstance(lang, Language)
        assert lang.phonology.openness == 0.75
        assert lang.phonology.stress == "initial"
        assert lang.phonotactics.onset == {"b": 4}
        assert lang.phonotactics.nucleus == {"a": 4}
        assert lang.phonotactics.coda == {"b": 1}
        assert lang.words == words


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

    def test_calculate_openness(self):
        words = ["/ba/", "/bab/", "/bwa/", "/ˈbwa.ma/"]
        assert Phonology.calculate_openness(words) == 0.8

    def test_poll_stress_initial(self):
        words = ["/ba/", "/ˈba.ba/", "/ˈba.bab.ba/", "/ba.ba.ba.ˈba/"]
        assert Phonology.poll_stress(words) == "initial"

    def test_poll_stress_final(self):
        words = ["/ba/", "/ˈba.ba/", "/bab.ba.ˈba/", "/ba.ba.ba.ˈba/"]
        assert Phonology.poll_stress(words) == "final"

    def test_poll_stress_penultimate(self):
        words = ["/ba/", "/ˈba.bab/", "/ba.ba.ˈba/", "/ba.ba.ˈba.ba/"]
        assert Phonology.poll_stress(words) == "penultimate"

    def test_poll_stress_antepenultimate(self):
        words = ["/ba/", "/ba.ˈba/", "/ˈba.bab.ba/", "/ba.ˈba.ba.ba/"]
        assert Phonology.poll_stress(words) == "antepenultimate"

    def test_poll_stress_heavy(self):
        words = ["/ba/", "/ˈba:.ba/", "/ba.ˈbab/", "/ˈba:b.ba:.bab.ba/", "/ba:.ˈba/"]
        assert Phonology.poll_stress(words) == "heavy"

    def test_poll_stress_random(self):
        words = ["/ba:.ˈba/", "/ˈba.ba:/", "/ba.ˈba.ba:.ba.ba/"]
        assert Phonology.poll_stress(words) == "random"

    def test_from_words(self):
        words = ["/ba/", "/ˈba.ba/"]
        phones = Phonology.from_words(words)
        assert isinstance(phones, Phonology)
        assert phones.openness == 1
        assert phones.stress == "initial"


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

    def test_from_words(self):
        words = ["/ba/", "/ˈba.ba/", "/bab/"]
        tactics = Phonotactics.from_words(words)
        assert isinstance(tactics, Phonotactics)
        assert tactics.onset == {"b": 4}
        assert tactics.nucleus == {"a": 4}
        assert tactics.coda == {"b": 1}


class TestStress:
    def test_creates_stress(self):
        stress = Stress()
        assert isinstance(stress, Stress)

    def test_defaults_initial(self):
        assert Stress() == "initial"

    def test_can_set_initial(self):
        assert Stress("initial") == "initial"

    def test_can_set_final(self):
        assert Stress("final") == "final"

    def test_can_set_penultimate(self):
        assert Stress("penultimate") == "penultimate"

    def test_can_set_antepenultimate(self):
        assert Stress("antepenultimate") == "antepenultimate"

    def test_can_set_heavy(self):
        assert Stress("heavy") == "heavy"

    def test_can_set_random(self):
        assert Stress("random") == "random"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            assert Stress("other") != "other"

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

    def test_is_initial(self):
        assert Stress.is_initial("/ba/") is True
        assert Stress.is_initial("/ˈba.ba/") is True
        assert Stress.is_initial("/ba.ˈba/") is False

    def test_is_final(self):
        assert Stress.is_final("/ba/") is True
        assert Stress.is_final("/ˈba.ba/") is False
        assert Stress.is_final("/ba.ˈba/") is True

    def test_is_penultimate(self):
        assert Stress.is_penultimate("/ba/") is True
        assert Stress.is_penultimate("/ˈba.ba/") is True
        assert Stress.is_penultimate("/ba.ˈba/") is False
        assert Stress.is_penultimate("/ˈba.ba.ba/") is False
        assert Stress.is_penultimate("/ba.ˈba.ba/") is True

    def test_is_antepenultimate(self):
        assert Stress.is_antepenultimate("/ba/") is True
        assert Stress.is_antepenultimate("/ˈba.ba/") is True
        assert Stress.is_antepenultimate("/ba.ˈba/") is False
        assert Stress.is_antepenultimate("/ˈba.ba.ba/") is True
        assert Stress.is_antepenultimate("/ba.ˈba.ba/") is False
        assert Stress.is_antepenultimate("/ˈba.ba.ba.ba/") is False
        assert Stress.is_antepenultimate("/ba.ˈba.ba.ba/") is True

    def test_is_heavy(self):
        assert Stress.is_heavy("/ba/") is True
        assert Stress.is_heavy("/ˈba.ba/") is True
        assert Stress.is_heavy("/ba.ˈba/") is True
        assert Stress.is_heavy("/ˈbab.ba/") is True
        assert Stress.is_heavy("/bab.ˈba/") is False
        assert Stress.is_heavy("/ˈba:.ba/") is True
        assert Stress.is_heavy("/ba:.ˈba/") is False
        assert Stress.is_heavy("/ˈbab.ba:.ba/") is True
        assert Stress.is_heavy("/bab.ˈba:.ba/") is True
        assert Stress.is_heavy("/bab.ba:.ˈba/") is False
        assert Stress.is_heavy("/ˈba:b.bab.ba:.ba/") is True
        assert Stress.is_heavy("/ba:b.ˈbab.ba:.ba/") is False
        assert Stress.is_heavy("/ba:b.bab.ˈba:.ba/") is False
        assert Stress.is_heavy("/ba:b.bab.ba:.ˈba/") is False

    def test_analyze_stress_monosyllabic(self):
        analysis = Stress.analyze_stress("/ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is True
        assert analysis["penultimate"] is True
        assert analysis["antepenultimate"] is True
        assert analysis["heavy"] is True

    def test_analyze_stress_bisyllabic1(self):
        analysis = Stress.analyze_stress("/ˈba.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is True
        assert analysis["antepenultimate"] is True
        assert analysis["heavy"] is True

    def test_analyze_stress_bisyllabic2(self):
        analysis = Stress.analyze_stress("/ba.ˈba/")
        assert analysis["initial"] is False
        assert analysis["final"] is True
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is True

    def test_analyze_stress_trisyllabic1(self):
        analysis = Stress.analyze_stress("/ˈba.ba.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is True
        assert analysis["heavy"] is True

    def test_analyze_stress_trisyllabic2(self):
        analysis = Stress.analyze_stress("/ba.ˈba.ba/")
        assert analysis["initial"] is False
        assert analysis["final"] is False
        assert analysis["penultimate"] is True
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is True

    def test_analyze_stress_trisyllabic3(self):
        analysis = Stress.analyze_stress("/ba.ba.ˈba/")
        assert analysis["initial"] is False
        assert analysis["final"] is True
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is True

    def test_analyze_stress_quatrosyllabic1(self):
        analysis = Stress.analyze_stress("/ˈba.ba.ba.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is True

    def test_analyze_stress_quatrosyllabic2(self):
        analysis = Stress.analyze_stress("/ba.ˈba.ba.ba/")
        assert analysis["initial"] is False
        assert analysis["final"] is False
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is True
        assert analysis["heavy"] is True

    def test_analyze_stress_quatrosyllabic3(self):
        analysis = Stress.analyze_stress("/ba.ba.ˈba.ba/")
        assert analysis["initial"] is False
        assert analysis["final"] is False
        assert analysis["penultimate"] is True
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is True

    def test_analyze_stress_quatrosyllabic4(self):
        analysis = Stress.analyze_stress("/ba.ba.ba.ˈba/")
        assert analysis["initial"] is False
        assert analysis["final"] is True
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is True

    def test_analyze_stress_heavy_long(self):
        analysis = Stress.analyze_stress("/ˈba:.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is True
        assert analysis["antepenultimate"] is True
        assert analysis["heavy"] is True

    def test_analyze_stress_not_heavy_long(self):
        analysis = Stress.analyze_stress("/ba:.ˈba/")
        assert analysis["initial"] is False
        assert analysis["final"] is True
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is False

    def test_analyze_stress_heavy_closed(self):
        analysis = Stress.analyze_stress("/ˈbab.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is True
        assert analysis["antepenultimate"] is True
        assert analysis["heavy"] is True

    def test_analyze_stress_not_heavy_closed(self):
        analysis = Stress.analyze_stress("/bab.ˈba/")
        assert analysis["initial"] is False
        assert analysis["final"] is True
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is False

    def test_analyze_stress_heavy_superheavy(self):
        analysis = Stress.analyze_stress("/ˈba:b.ba:.bab.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is True

    def test_analyze_stress_heavy_superheavy_long(self):
        analysis = Stress.analyze_stress("/ˈba:.ba:b.bab.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is False

    def test_analyze_stress_heavy_superheavy_closed(self):
        analysis = Stress.analyze_stress("/ˈbab.ba:.ba:b.ba/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is False

    def test_analyze_stress_heavy_superheavy_light(self):
        analysis = Stress.analyze_stress("/ˈba.ba:.bab.ba:b/")
        assert analysis["initial"] is True
        assert analysis["final"] is False
        assert analysis["penultimate"] is False
        assert analysis["antepenultimate"] is False
        assert analysis["heavy"] is False
