from typing import List, Optional
from language.classes import Language


class History:
    def __init__(self, lang: Optional[Language] = None):
        self.log: List[str] = []
        self.stages: List[List[str]] = []
        if lang is not None:
            self.stages.append(lang.words)
