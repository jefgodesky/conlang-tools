import pytest
from phonemes.vowels import Vowel, VowelLocation, VowelOpenness


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


class TestVowelLocation:
    def test_creates_vowel_location(self):
        location = VowelLocation()
        assert isinstance(location, VowelLocation)

    def test_defaults_front(self):
        location = VowelLocation()
        assert location == "front"

    def test_can_set_front(self):
        location = VowelLocation("front")
        assert location == "front"

    def test_can_set_central(self):
        location = VowelLocation("central")
        assert location == "central"

    def test_can_set_back(self):
        location = VowelLocation("back")
        assert location == "back"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            location = VowelLocation("other")
            assert location != "other"

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
        openness = VowelOpenness()
        assert openness == "close"

    def test_can_set_open(self):
        openness = VowelOpenness("open")
        assert openness == "open"

    def test_can_set_near_open(self):
        openness = VowelOpenness("near-open")
        assert openness == "near-open"

    def test_can_set_open_mid(self):
        openness = VowelOpenness("open-mid")
        assert openness == "open-mid"

    def test_can_set_mid(self):
        openness = VowelOpenness("mid")
        assert openness == "mid"

    def test_can_set_close_mid(self):
        openness = VowelOpenness("close-mid")
        assert openness == "close-mid"

    def test_can_set_near_close(self):
        openness = VowelOpenness("near-close")
        assert openness == "near-close"

    def test_can_set_close(self):
        openness = VowelOpenness("close")
        assert openness == "close"

    def test_rejects_other(self):
        with pytest.raises(TypeError):
            openness = VowelOpenness("other")
            assert openness == "other"

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
