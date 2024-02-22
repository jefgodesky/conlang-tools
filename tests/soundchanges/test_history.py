import csv
import io
import pytest
from language.classes import Language, Phonology, Phonotactics
from soundchanges.history import History


class TestHistory:
    @pytest.fixture
    def example_language(self):
        pt = Phonotactics(onset={"b": 1}, nucleus={"a": 1, "o": 1}, coda={"b": 1})
        pl = Phonology(stress="initial", openness=1)
        return Language(phonotactics=pt, phonology=pl, words=["/ˈba.ba/", "/ba/"])

    @pytest.fixture
    def example_history(self, example_language):
        return History(example_language)

    def test_sets_language(self, example_history, example_language):
        assert example_history.language == example_language

    def test_creates_history(self, example_history):
        assert isinstance(example_history, History)

    def test_sets_up_log(self, example_history):
        assert len(example_history.log) == 0

    def test_takes_language(self, example_history):
        assert len(example_history.stages) == 1
        assert example_history.stages[0][0] == "/ˈba.ba/"
        assert example_history.stages[0][1] == "/ba/"

    def test_step(self, example_history, example_language):
        example_history.step()
        assert len(example_history.log) == 1
        assert len(example_history.stages) == 2
        assert len(example_history.stages[1]) == len(example_language.words)

    def test_csv(self, example_history):
        example_history.step()
        example_history.step()
        example_history.step()
        csv_str = example_history.to_csv()
        obj = io.StringIO(csv_str)
        reader = csv.reader(obj)
        next(reader)
        first_row = next(reader)
        assert example_history.stages[3][0] is not None
        assert first_row[3] == str(example_history.stages[3][0])
        obj.close()
