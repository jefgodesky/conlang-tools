import pytest
from conlang_tools.phonemes.vowels import (
    Vowel,
    VowelLocation,
    VowelOpenness,
)
from conlang_tools.tests.phonemes.test_collections import TestGetVowel


class TestVowel:
    def test_creates_vowel(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False)
        TestGetVowel.isi(i)

    def test_repr(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False)
        assert str(i) == "[i]"

    def test_repr_long(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, long=True)
        assert str(i) == "[i:]"

    def test_same_except(self):
        # fmt: off
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, long=False)
        il = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, long=True)
        y = Vowel("y", VowelOpenness("close"), VowelLocation("front"), True, long=False)
        e = Vowel("e", VowelOpenness("close-mid"), VowelLocation("front"), False, long=False)
        el = Vowel("e:", VowelOpenness("close-mid"), VowelLocation("front"), False, long=True)
        w = Vowel("ɯ", VowelOpenness("close"), VowelLocation("back"), False, long=False)
        u = Vowel("u", VowelOpenness("close"), VowelLocation("back"), True, long=False)
        # fmt: on

        assert i.same_except(il, "length") is True
        assert i.same_except(y, "roundedness") is True
        assert i.same_except(e, "height") is True
        assert i.same_except(el, "height") is False
        assert i.same_except(w, "location") is True
        assert i.same_except(u, "location") is False


class TestVowelLocation:
    def test_creates_vowel_location(self):
        location = VowelLocation()
        assert isinstance(location, VowelLocation)

    def test_defaults_front(self):
        assert VowelLocation() == "front"

    def test_can_set_front(self):
        assert VowelLocation("front") == "front"

    def test_can_set_central(self):
        assert VowelLocation("central") == "central"

    def test_can_set_back(self):
        assert VowelLocation("back") == "back"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            assert VowelLocation("other") != "other"

    def test_returns_types(self):
        expected = "front, central, back"
        assert ", ".join(VowelLocation.types()) == expected

    def test_is_valid_front_true(self):
        assert VowelLocation.is_valid("front") is True

    def test_is_valid_central_true(self):
        assert VowelLocation.is_valid("central") is True

    def test_is_valid_back_true(self):
        assert VowelLocation.is_valid("back") is True

    def test_is_valid_other_false(self):
        assert VowelLocation.is_valid("other") is False

    def test_forward_back(self):
        assert VowelLocation.forward("back") == "central"

    def test_forward_central(self):
        assert VowelLocation.forward("central") == "front"

    def test_forward_front(self):
        assert VowelLocation.forward("front") == "front"

    def test_backward_back(self):
        assert VowelLocation.backward("back") == "back"

    def test_backward_central(self):
        assert VowelLocation.backward("central") == "back"

    def test_backward_front(self):
        assert VowelLocation.backward("front") == "central"


class TestVowelOpenness:
    def test_creates_vowel_openness(self):
        openness = VowelOpenness()
        assert isinstance(openness, VowelOpenness)

    def test_defaults_close(self):
        assert VowelOpenness() == "close"

    def test_can_set_open(self):
        assert VowelOpenness("open") == "open"

    def test_can_set_near_open(self):
        assert VowelOpenness("near-open") == "near-open"

    def test_can_set_open_mid(self):
        assert VowelOpenness("open-mid") == "open-mid"

    def test_can_set_mid(self):
        assert VowelOpenness("mid") == "mid"

    def test_can_set_close_mid(self):
        assert VowelOpenness("close-mid") == "close-mid"

    def test_can_set_near_close(self):
        assert VowelOpenness("near-close") == "near-close"

    def test_can_set_close(self):
        assert VowelOpenness("close") == "close"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            assert VowelOpenness("other") == "other"

    def test_returns_types(self):
        expected = "close, near-close, close-mid, mid, open-mid, near-open, open"
        assert ", ".join(VowelOpenness.types()) == expected

    def test_is_valid_close_true(self):
        assert VowelOpenness.is_valid("close") is True

    def test_is_valid_near_close_true(self):
        assert VowelOpenness.is_valid("near-close") is True

    def test_is_valid_close_mid_true(self):
        assert VowelOpenness.is_valid("close-mid") is True

    def test_is_valid_mid_true(self):
        assert VowelOpenness.is_valid("mid") is True

    def test_is_valid_open_mid_true(self):
        assert VowelOpenness.is_valid("open-mid") is True

    def test_is_valid_near_open_true(self):
        assert VowelOpenness.is_valid("near-open") is True

    def test_is_valid_open_true(self):
        assert VowelOpenness.is_valid("open") is True

    def test_is_valid_other_false(self):
        assert VowelOpenness.is_valid("other") is False

    def test_higher_open(self):
        assert VowelOpenness.higher("open") == "near-open"

    def test_higher_near_open(self):
        assert VowelOpenness.higher("near-open") == "open-mid"

    def test_higher_open_mid(self):
        assert VowelOpenness.higher("open-mid") == "mid"

    def test_higher_mid(self):
        assert VowelOpenness.higher("mid") == "close-mid"

    def test_higher_closer_mid(self):
        assert VowelOpenness.higher("close-mid") == "near-close"

    def test_higher_near_close(self):
        assert VowelOpenness.higher("near-close") == "close"

    def test_higher_close(self):
        assert VowelOpenness.higher("close") == "close"

    def test_lower_open(self):
        assert VowelOpenness.lower("open") == "open"

    def test_lower_near_open(self):
        assert VowelOpenness.lower("near-open") == "open"

    def test_lower_open_mid(self):
        assert VowelOpenness.lower("open-mid") == "near-open"

    def test_lower_mid(self):
        assert VowelOpenness.lower("mid") == "open-mid"

    def test_lower_close_mid(self):
        assert VowelOpenness.lower("close-mid") == "mid"

    def test_lower_near_close(self):
        assert VowelOpenness.lower("near-close") == "close-mid"

    def test_lower_close(self):
        assert VowelOpenness.lower("close") == "near-close"
