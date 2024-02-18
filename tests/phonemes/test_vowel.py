import pytest
from phonemes.vowels import Vowel, VowelLocation, VowelOpenness, get_vowels, get_vowel


class TestGetVowels:
    def test_get_vowels(self):
        vowels = get_vowels()
        assert len(vowels) == 33
        assert all(isinstance(vowel, Vowel) for vowel in vowels)


class TestGetVowel:
    def test_get_vowel(self):
        i = get_vowel("i")
        assert isinstance(i, Vowel)
        assert i.symbol == "i"
        assert i.openness == "close"
        assert isinstance(i.openness, VowelOpenness)
        assert i.location == "front"
        assert isinstance(i.location, VowelLocation)
        assert i.rounded is False

    def test_returns_none_if_not_found(self):
        assert get_vowel("@") is None


class TestVowel:
    def test_creates_vowel(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False)
        assert isinstance(i, Vowel)
        assert i.symbol == "i"
        assert i.openness == "close"
        assert isinstance(i.openness, VowelOpenness)
        assert i.location == "front"
        assert isinstance(i.location, VowelLocation)
        assert i.rounded is False

    def test_repr(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False)
        assert str(i) == "[i]"


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

    def test_islocation_front_true(self):
        assert VowelLocation.islocation("front") is True

    def test_islocation_central_true(self):
        assert VowelLocation.islocation("central") is True

    def test_islocation_back_true(self):
        assert VowelLocation.islocation("back") is True

    def test_islocation_other_false(self):
        assert VowelLocation.islocation("other") is False


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

    def test_isopenness_close_true(self):
        assert VowelOpenness.isopenness("close") is True

    def test_isopenness_near_close_true(self):
        assert VowelOpenness.isopenness("near-close") is True

    def test_isopenness_close_mid_true(self):
        assert VowelOpenness.isopenness("close-mid") is True

    def test_isopenness_mid_true(self):
        assert VowelOpenness.isopenness("mid") is True

    def test_isopenness_open_mid_true(self):
        assert VowelOpenness.isopenness("open-mid") is True

    def test_isopenness_near_open_true(self):
        assert VowelOpenness.isopenness("near-open") is True

    def test_isopenness_open_true(self):
        assert VowelOpenness.isopenness("open") is True

    def test_isopenness_other_false(self):
        assert VowelOpenness.isopenness("other") is False
