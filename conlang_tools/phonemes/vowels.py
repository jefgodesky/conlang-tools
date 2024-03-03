from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Literal, Optional, TypeVar

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update VowelOpenness.types and/or VowelLocation.types to match!
VowelOpennessTypes = Literal[
    "close", "near-close", "close-mid", "mid", "open-mid", "near-open", "open"
]
VowelLocationTypes = Literal["front", "central", "back"]
VowelAttributeTypes = TypeVar("VowelAttributeTypes")


class VowelAttribute(ABC, Generic[VowelAttributeTypes]):
    def __init__(self, value: Optional[str] = None):
        types = self.types()
        self.value = value if value is not None else types[0]
        if not self.is_valid(self.value):
            raise TypeError(
                f"{self.value} is not a valid value. Choose one of: {', '.join(types)}."
            )

    def __eq__(self, other):
        return self.value == other

    @classmethod
    @abstractmethod
    def types(cls) -> List[VowelAttributeTypes]:
        pass

    @classmethod
    def is_valid(cls, candidate: str) -> bool:
        return candidate in cls.types()

    @classmethod
    def adjacent(
        cls, ref: VowelAttributeTypes, direction: int = -1
    ) -> VowelAttributeTypes:
        types = cls.types()
        clamp = max if direction == -1 else min
        limit = 0 if direction == -1 else len(types) - 1
        return types[clamp(types.index(ref) + direction, limit)]


class VowelLocation(VowelAttribute[VowelLocationTypes]):
    @classmethod
    def types(cls) -> List[VowelLocationTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update VowelLocationTypes to match!
        return ["front", "central", "back"]

    @classmethod
    def forward(cls, ref: VowelLocationTypes) -> VowelLocationTypes:
        return cls.adjacent(ref, -1)

    @classmethod
    def backward(cls, ref: VowelLocationTypes) -> VowelLocationTypes:
        return cls.adjacent(ref, 1)


class VowelOpenness(VowelAttribute[VowelOpennessTypes]):
    @classmethod
    def types(cls) -> List[VowelOpennessTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update VowelOpennessTypes to match!
        return [
            "close",
            "near-close",
            "close-mid",
            "mid",
            "open-mid",
            "near-open",
            "open",
        ]

    @classmethod
    def higher(cls, ref: VowelOpennessTypes) -> VowelOpennessTypes:
        return cls.adjacent(ref, -1)

    @classmethod
    def lower(cls, ref: VowelOpennessTypes) -> VowelOpennessTypes:
        return cls.adjacent(ref, 1)


@dataclass(frozen=True, order=True)
class Vowel:
    symbol: str
    openness: VowelOpenness
    location: VowelLocation
    rounded: bool
    long: Optional[bool] = False

    def __repr__(self):
        return f"[{self.symbol}:]" if self.long else f"[{self.symbol}]"

    def __hash__(self):
        return hash(self.symbol)

    def same_except(self, other: "Vowel", criterion: str = "height") -> bool:
        comparisons = {
            "height": self.openness == other.openness,
            "location": self.location == other.location,
            "roundedness": self.rounded == other.rounded,
            "length": self.long == other.long,
        }
        return all([value for key, value in comparisons.items() if key != criterion])
