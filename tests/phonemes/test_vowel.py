import pytest
from phonemes.vowels import VowelOpenness


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
