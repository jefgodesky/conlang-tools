from typing import List, Literal, Optional

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update ConsonantPlace.types to match!
ConsonantPlaceTypes = Literal["labial", "dental", "alveolar-central", "alveolar-lateral", "retroflex", "palatal", "post-alveolar", "velar", "uvular", "pharyngeal", "glottal"]


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
