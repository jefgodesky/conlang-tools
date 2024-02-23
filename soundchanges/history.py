import csv
import io
from typing import List
from language.classes import Language
from soundchanges.changes import change


class History:
    def __init__(self, lang: Language):
        self.language = lang
        self.log: List[str] = []
        self.stages: List[List[str]] = []
        if lang is not None:
            self.stages.append(lang.words)

    def step(self):
        description, words = change(self.language)
        self.log.append(description)
        self.stages.append(words)
        return description, words

    def to_csv(self) -> str:
        headers = ["Original"] + [f"Change {i}" for i in range(1, len(self.stages))]
        rows = list(zip(*self.stages))
        output = io.StringIO()
        try:
            csv_writer = csv.writer(output)
            csv_writer.writerow(headers)
            csv_writer.writerows(rows)
            return output.getvalue()
        finally:
            output.close()
