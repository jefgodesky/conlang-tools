from soundchanges.soundchange import SoundChange


class TestSoundChange:
    def test_has_description(self):
        assert SoundChange.description == "No change."

    def test_has_weight(self):
        assert SoundChange.weight == 1

    def test_apply(self):
        original = "/ba/"
        assert SoundChange.apply(original) == original

    def test_apply_list(self):
        original = ["/ba/"]
        assert SoundChange.apply_list(original) == original
