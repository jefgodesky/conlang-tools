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


def get_vowels() -> List[Vowel]:
    # fmt: off
    short = [
        Vowel("i", VowelOpenness("close"), VowelLocation("front"), False),
        Vowel("y", VowelOpenness("close"), VowelLocation("front"), True),
        Vowel("ɨ", VowelOpenness("close"), VowelLocation("central"), False),
        Vowel("ʉ", VowelOpenness("close"), VowelLocation("central"), True),
        Vowel("ɯ", VowelOpenness("close"), VowelLocation("back"), False),
        Vowel("u", VowelOpenness("close"), VowelLocation("back"), True),
        Vowel("ɪ", VowelOpenness("near-close"), VowelLocation("front"), False),
        Vowel("ʏ", VowelOpenness("near-close"), VowelLocation("front"), True),
        Vowel("ʊ", VowelOpenness("near-close"), VowelLocation("back"), True),
        Vowel("e", VowelOpenness("close-mid"), VowelLocation("front"), False),
        Vowel("ø", VowelOpenness("close-mid"), VowelLocation("front"), True),
        Vowel("ɘ", VowelOpenness("close-mid"), VowelLocation("central"), False),
        Vowel("ɵ", VowelOpenness("close-mid"), VowelLocation("central"), True),
        Vowel("ɤ", VowelOpenness("close-mid"), VowelLocation("back"), False),
        Vowel("o", VowelOpenness("close-mid"), VowelLocation("back"), True),
        Vowel("e̞", VowelOpenness("mid"), VowelLocation("front"), False),
        Vowel("ø̞̞", VowelOpenness("mid"), VowelLocation("front"), True),
        Vowel("ə", VowelOpenness("mid"), VowelLocation("front"), False),
        Vowel("ɤ̞", VowelOpenness("mid"), VowelLocation("back"), False),
        Vowel("o̞", VowelOpenness("mid"), VowelLocation("back"), True),
        Vowel("ɛ", VowelOpenness("open-mid"), VowelLocation("front"), False),
        Vowel("œ", VowelOpenness("open-mid"), VowelLocation("front"), True),
        Vowel("ɜ", VowelOpenness("open-mid"), VowelLocation("central"), False),
        Vowel("ɞ", VowelOpenness("open-mid"), VowelLocation("central"), True),
        Vowel("ʌ", VowelOpenness("open-mid"), VowelLocation("back"), False),
        Vowel("ɔ", VowelOpenness("open-mid"), VowelLocation("back"), True),
        Vowel("æ", VowelOpenness("near-open"), VowelLocation("front"), False),
        Vowel("ɐ", VowelOpenness("near-open"), VowelLocation("central"), False),
        Vowel("a", VowelOpenness("open"), VowelLocation("front"), False),
        Vowel("ɶ", VowelOpenness("open"), VowelLocation("front"), True),
        Vowel("ä", VowelOpenness("open"), VowelLocation("central"), False),
        Vowel("ɑ", VowelOpenness("open"), VowelLocation("back"), False),
        Vowel("ɒ", VowelOpenness("open"), VowelLocation("back"), True),
    ]
    # fmt: on

    long = [
        Vowel(v.symbol + ":", v.openness, v.location, v.rounded, long=True)
        for v in short
    ]
    return long + short


def get_vowel(symbol: str) -> Optional[Vowel]:
    vowels = get_vowels()
    symbols = [vowel.symbol for vowel in vowels]
    try:
        index = symbols.index(symbol)
        return vowels[index]
    except ValueError:
        return None


def find_vowel(
    openness: VowelOpennessTypes,
    location: VowelLocationTypes,
    rounded: bool,
    long: bool,
) -> Optional[Vowel]:
    vowels = get_vowels()
    for vowel in vowels:
        matches = [
            vowel.openness == openness,
            vowel.location == location,
            vowel.rounded == rounded,
            vowel.long == long,
        ]
        if all(matches):
            return vowel
    return None


def find_similar_vowel(
    vowel: Vowel,
    openness: Optional[VowelOpennessTypes] = None,
    location: Optional[VowelLocationTypes] = None,
    rounded: Optional[bool] = None,
    long: Optional[bool] = None,
) -> Optional[Vowel]:
    openness_arg = openness if openness is not None else vowel.openness.value
    location_arg = location if location is not None else vowel.location.value
    rounded_arg = rounded if rounded is not None else vowel.rounded
    long_arg = long if long is not None else vowel.long
    return find_vowel(
        openness=openness_arg,
        location=location_arg,
        rounded=rounded_arg,
        long=long_arg,
    )
