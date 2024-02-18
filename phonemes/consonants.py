from typing import List, Literal, Optional

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update ConsonantPlace.types and/or ConsonantManner.types to match!
ConsonantPlaceTypes = Literal["labial", "dental", "alveolar-central", "alveolar-lateral", "retroflex", "palatal", "post-alveolar", "velar", "uvular", "pharyngeal", "glottal"]
ConsonantMannerTypes = Literal["stop", "fricative", "affricate", "nasal", "liquid"]
ConsonantCategory = Literal["obstruent", "resonant", "n/a"]


class ConsonantManner:
    def __init__(self, value: Optional[ConsonantMannerTypes] = None):
        types = ConsonantManner.types()
        self.value = value if value is not None else types[0]
        if not ConsonantManner.ismanner(self.value):
            raise TypeError(f"{self.value} is not a valid value for ConsonantManner. Choose one of: {', '.join(types)}.")

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def types(cls) -> List[ConsonantMannerTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update ConsonantMannerTypes to match!
        return ["stop", "fricative", "affricate", "nasal", "liquid"]

    @classmethod
    def ismanner(cls, candidate: str) -> bool:
        return candidate in cls.types()

    @staticmethod
    def category(manner: ConsonantMannerTypes) -> ConsonantCategory:
        categories = {
            "stop": "obstruent",
            "fricative": "obstruent",
            "affricate": "obstruent",
            "nasal": "resonant",
            "liquid": "resonant"
        }
        return categories[manner] if manner in categories else "n/a"


class ConsonantPlace:
    def __init__(self, value: Optional[ConsonantPlaceTypes] = None):
        types = ConsonantPlace.types()
        self.value = value if value is not None else types[0]
        if not ConsonantPlace.isplace(self.value):
            raise TypeError(f"{self.value} is not a valid value for ConsonantPlace. Choose one of: {', '.join(types)}.")

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def types(cls) -> List[ConsonantPlaceTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update ConsonantPlaceTypes to match!
        return ["labial", "dental", "alveolar-central", "alveolar-lateral", "retroflex", "palatal", "post-alveolar", "velar", "uvular", "pharyngeal", "glottal"]

    @classmethod
    def isplace(cls, candidate: str) -> bool:
        return candidate in cls.types()
