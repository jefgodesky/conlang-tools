from typing import List, Optional


class History:
    def __init__(self, words: Optional[List[str]] = None):
        self.log: List[str] = []
        self.stages: List[List[str]] = []
        if words is not None:
            self.stages.append(words)
