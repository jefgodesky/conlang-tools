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
