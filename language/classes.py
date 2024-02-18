from typing import Dict, List, Literal, Optional

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update Stress.types to match!
StressTypes = Literal["initial", "final", "penultimate", "antepenultimate", "heavy", "random"]


class Phonology:
    def __init__(self, stress: Optional[StressTypes] = None, openness: float = 0.5):
        self.stress = Stress(stress)
        self.openness = openness


class Phonotactics:
    def __init__(
            self,
            onset: Optional[Dict[str, int]] = None,
            nucleus: Optional[Dict[str, int]] = None,
            coda: Optional[Dict[str, int]] = None
    ):
        self.onset = onset if onset is not None else {}
        self.nucleus = nucleus if nucleus is not None else {}
        self.coda = coda if coda is not None else {}


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

