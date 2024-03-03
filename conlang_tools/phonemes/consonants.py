from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Literal, Optional, TypeVar
from conlang_tools.phonemes.phonemes import Phoneme

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update ConsonantPlace.types and/or ConsonantManner.types to match!
ConsonantPlaceTypes = Literal[
    "labial",
    "dental",
    "alveolar-central",
    "alveolar-lateral",
    "retroflex",
    "palatal",
    "post-alveolar",
    "velar",
    "uvular",
    "pharyngeal",
    "glottal",
]
ConsonantMannerTypes = Literal["stop", "fricative", "affricate", "nasal", "liquid"]
ConsonantCategory = Literal["obstruent", "resonant", "n/a"]
ConsonantAttributeTypes = TypeVar("ConsonantAttributeTypes")


class ConsonantAttribute(ABC, Generic[ConsonantAttributeTypes]):
    def __init__(self, value: Optional[str] = None):
        types = self.types()
        self.value = value if value is not None else types[0]
        if not self.is_valid(self.value):
            raise TypeError(
                f"{self.value} is not a valid value. Choose one of: {', '.join(types)}."
            )

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)

    @classmethod
    @abstractmethod
    def types(cls) -> List[ConsonantAttributeTypes]:
        pass

    @classmethod
    def is_valid(cls, candidate: str) -> bool:
        return candidate in cls.types()


class ConsonantManner(ConsonantAttribute[ConsonantMannerTypes]):
    @classmethod
    def types(cls) -> List[ConsonantMannerTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update ConsonantMannerTypes to match!
        return ["stop", "fricative", "affricate", "nasal", "liquid"]

    @staticmethod
    def category(manner: ConsonantMannerTypes) -> ConsonantCategory:
        categories = {
            "stop": "obstruent",
            "fricative": "obstruent",
            "affricate": "obstruent",
            "nasal": "resonant",
            "liquid": "resonant",
        }
        return categories[manner] if manner in categories else "n/a"


class ConsonantPlace(ConsonantAttribute[ConsonantPlaceTypes]):
    @classmethod
    def types(cls) -> List[ConsonantPlaceTypes]:
        # Sadly, we can't automate list-to-literal, so if you update this list,
        # make sure you update ConsonantPlaceTypes to match!
        return [
            "labial",
            "dental",
            "alveolar-central",
            "alveolar-lateral",
            "retroflex",
            "palatal",
            "post-alveolar",
            "velar",
            "uvular",
            "pharyngeal",
            "glottal",
        ]


@dataclass(frozen=True, order=True, repr=False)
class Consonant(Phoneme):
    manner: ConsonantManner
    place: ConsonantPlace
    voiced: bool

    @property
    def category(self):
        return ConsonantManner.category(self.manner.value)

    def is_sibilant(self) -> bool:
        manners = ["fricative", "affricate"]
        places = ["dental", "alveolar-central", "post-alveolar"]
        return self.manner in manners and self.place in places
