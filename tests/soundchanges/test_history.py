import pytest
from language.classes import Language, Phonology, Phonotactics
from soundchanges.history import History


class TestHistory:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "o": 1}, coda={"b": 1})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ˈba.ba/", "/ba/"])

    def test_creates_history(self):
        history = History()
        assert isinstance(history, History)

    def test_sets_up_log(self):
        history = History()
        assert len(history.log) == 0

    def test_takes_language(self, example_language):
        history = History(example_language)
        assert len(history.stages) == 1
        assert history.stages[0][0] == "/ˈba.ba/"
        assert history.stages[0][1] == "/ba/"
