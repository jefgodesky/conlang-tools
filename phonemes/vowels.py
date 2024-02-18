from typing import List, Literal, Optional

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update VowelOpenness.types to match!
VowelOpennessTypes = Literal["close", "near-close", "close-mid", "mid", "open-mid", "near-open", "open"]


class VowelOpenness:
    def __init__(self, value: Optional[VowelOpennessTypes] = None):
        types = VowelOpenness.types()
        self.value = value if value is not None else types[0]
        if not VowelOpenness.isopenness(self.value):
            raise TypeError(f"{self.value} is not a valid value for VowelOpenness. Choose one of: {', '.join(types)}.")

    def __eq__(self, other):
        return self.value == other

    @classmethod
    def types(cls) -> List[VowelOpennessTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update VowelOpennessTypes to match!
        return ["close", "near-close", "close-mid", "mid", "open-mid", "near-open", "open"]

    @classmethod
    def isopenness(cls, candidate: str) -> bool:
        return candidate in cls.types()