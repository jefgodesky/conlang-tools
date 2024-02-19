from soundchanges.describe import oxford_comma


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
