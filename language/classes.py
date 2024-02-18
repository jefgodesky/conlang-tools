from typing import List, Literal, Optional

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update Stress.types to match!
StressTypes = Literal["initial", "final", "penultimate", "antepenultimate", "heavy", "random"]


class Stress:
    def __init__(self, value: Optional[StressTypes] = None):
        types = Stress.types()
        self.value = value if value is not None else types[0]
        if not Stress.isstress(self.value):
            raise TypeError(f"{self.value} is not a valid value for Stress. Choose one of: {', '.join(types)}.")

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def types(cls) -> List[StressTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update StressTypes to match!
        return ["initial", "final", "penultimate", "antepenultimate", "heavy", "random"]

    @classmethod
    def isstress(cls, candidate: str) -> bool:
        return candidate in cls.types()

