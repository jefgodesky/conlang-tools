from soundchanges.history import History


class TestHistory:
    def test_creates_history(self):
        history = History()
        assert isinstance(history, History)

    def test_sets_up_log(self):
        history = History()
        assert len(history.log) == 0

    def test_takes_words(self):
        history = History(["/ba/"])
        assert len(history.stages) == 1
        assert history.stages[0][0] == "/ba/"
