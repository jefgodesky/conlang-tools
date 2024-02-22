from typing import List
from language.classes import Language


class History:
    def __init__(self, lang: Language):
        self.language = lang
        self.log: List[str] = []
        self.stages: List[List[str]] = []
        if lang is not None:
            self.stages.append(lang.words)
