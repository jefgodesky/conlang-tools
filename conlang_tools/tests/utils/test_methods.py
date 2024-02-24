from conlang_tools.utils.methods import (
    get_choices,
    oxford_comma,
    weigh_syllable,
    weigh_syllables,
)


class TestGetChoices:
    def test_returns_list(self):
        dictionary = {"a": 3, "b": 2, "c": 1}
        assert "-".join(get_choices(dictionary)) == "a-a-a-b-b-c"


class TestOxfordComma:
    def test_empty_list(self):
        assert oxford_comma([]) == ""

    def test_one_item(self):
        assert oxford_comma(["this"]) == "this"

    def test_two_items(self):
        assert oxford_comma(["this", "that"]) == "this and that"

    def test_three_items(self):
        expected = "this, that, and the other"
        assert oxford_comma(["this", "that", "the other"]) == expected


class TestWeighSyllable:
    def test_weigh_syllable_normal_0(self):
        assert weigh_syllable("ba") == 0

    def test_weigh_syllable_long_vowel_1(self):
        assert weigh_syllable("ba:") == 1

    def test_weigh_syllable_consonant_coda_1(self):
        assert weigh_syllable("bab") == 1

    def test_weigh_syllable_superheavy_2(self):
        assert weigh_syllable("ba:b") == 2

    def test_weigh_syllables(self):
        weights = weigh_syllables(["ba", "ba:", "bab", "ba:b"])
        assert weights == [0, 1, 1, 2]
