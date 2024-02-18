from typing import List


class SoundChange:
    description = "No change."
    weight = 1

    @staticmethod
    def apply(word: str) -> str:
        return word

    @classmethod
    def apply_list(cls, words: List[str]) -> List[str]:
        return [cls.apply(word) for word in words]
