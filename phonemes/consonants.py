from dataclasses import dataclass
from typing import List, Literal, Optional

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


class ConsonantManner:
    def __init__(self, value: Optional[ConsonantMannerTypes] = None):
        types = ConsonantManner.types()
        self.value = value if value is not None else types[0]
        if not ConsonantManner.ismanner(self.value):
            raise TypeError(
                f"{self.value} is not a valid value for ConsonantManner. Choose one of: {', '.join(types)}."
            )

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
            "liquid": "resonant",
        }
        return categories[manner] if manner in categories else "n/a"


class ConsonantPlace:
    def __init__(self, value: Optional[ConsonantPlaceTypes] = None):
        types = ConsonantPlace.types()
        self.value = value if value is not None else types[0]
        if not ConsonantPlace.isplace(self.value):
            raise TypeError(
                f"{self.value} is not a valid value for ConsonantPlace. Choose one of: {', '.join(types)}."
            )

    def __eq__(self, other):
        return self.value == other

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

    @classmethod
    def isplace(cls, candidate: str) -> bool:
        return candidate in cls.types()


@dataclass(frozen=True, order=True)
class Consonant:
    symbol: str
    manner: ConsonantManner
    place: ConsonantPlace
    voiced: bool

    @property
    def category(self):
        return ConsonantManner.category(self.manner.value)

    def __repr__(self):
        return f"[{self.symbol}]"


def get_consonants() -> List[Consonant]:
    # fmt: off
    return [
        # Obstruents > Stops
        Consonant("p", ConsonantManner("stop"), ConsonantPlace("labial"), False),
        Consonant("b", ConsonantManner("stop"), ConsonantPlace("labial"), True),
        Consonant("t̼", ConsonantManner("stop"), ConsonantPlace("dental"), False),
        Consonant("d̼", ConsonantManner("stop"), ConsonantPlace("dental"), True),
        Consonant("t", ConsonantManner("stop"), ConsonantPlace("alveolar-central"), False),
        Consonant("d", ConsonantManner("stop"), ConsonantPlace("alveolar-central"), True),
        Consonant("ʈ", ConsonantManner("stop"), ConsonantPlace("retroflex"), False),
        Consonant("ɖ", ConsonantManner("stop"), ConsonantPlace("retroflex"), True),
        Consonant("c", ConsonantManner("stop"), ConsonantPlace("palatal"), False),
        Consonant("ɟ", ConsonantManner("stop"), ConsonantPlace("palatal"), True),
        Consonant("k", ConsonantManner("stop"), ConsonantPlace("velar"), False),
        Consonant("g", ConsonantManner("stop"), ConsonantPlace("velar"), True),
        Consonant("q", ConsonantManner("stop"), ConsonantPlace("uvular"), False),
        Consonant("ɢ", ConsonantManner("stop"), ConsonantPlace("uvular"), True),
        Consonant("ʔ", ConsonantManner("stop"), ConsonantPlace("glottal"), False),
        # Obstruents > Fricatives
        Consonant("f", ConsonantManner("fricative"), ConsonantPlace("labial"), False),
        Consonant("v", ConsonantManner("fricative"), ConsonantPlace("labial"), True),
        Consonant("θ", ConsonantManner("fricative"), ConsonantPlace("dental"), False),
        Consonant("ð", ConsonantManner("fricative"), ConsonantPlace("dental"), True),
        Consonant("s", ConsonantManner("fricative"), ConsonantPlace("alveolar-central"), False),
        Consonant("z", ConsonantManner("fricative"), ConsonantPlace("alveolar-central"), True),
        Consonant("ɬ", ConsonantManner("fricative"), ConsonantPlace("alveolar-lateral"), False),
        Consonant("ɮ", ConsonantManner("fricative"), ConsonantPlace("alveolar-lateral"), True),
        Consonant("ʂ", ConsonantManner("fricative"), ConsonantPlace("retroflex"), False),
        Consonant("ʐ", ConsonantManner("fricative"), ConsonantPlace("retroflex"), True),
        Consonant("ç", ConsonantManner("fricative"), ConsonantPlace("palatal"), False),
        Consonant("ʝ", ConsonantManner("fricative"), ConsonantPlace("palatal"), True),
        Consonant("ʃ", ConsonantManner("fricative"), ConsonantPlace("post-alveolar"), False),
        Consonant("ʒ", ConsonantManner("fricative"), ConsonantPlace("post-alveolar"), True),
        Consonant("x", ConsonantManner("fricative"), ConsonantPlace("velar"), False),
        Consonant("ɣ", ConsonantManner("fricative"), ConsonantPlace("velar"), True),
        Consonant("χ", ConsonantManner("fricative"), ConsonantPlace("uvular"), False),
        Consonant("ʁ", ConsonantManner("fricative"), ConsonantPlace("uvular"), True),
        Consonant("ħ", ConsonantManner("fricative"), ConsonantPlace("pharyngeal"), False),
        Consonant("ʕ", ConsonantManner("fricative"), ConsonantPlace("pharyngeal"), True),
        Consonant("h", ConsonantManner("fricative"), ConsonantPlace("glottal"), False),
        Consonant("ɦ", ConsonantManner("fricative"), ConsonantPlace("glottal"), True),
        # Obstruents > Affricates
        Consonant("pf", ConsonantManner("affricate"), ConsonantPlace("labial"), False),
        Consonant("bv", ConsonantManner("affricate"), ConsonantPlace("labial"), True),
        Consonant("t̪θ", ConsonantManner("affricate"), ConsonantPlace("dental"), False),
        Consonant("d̪ð", ConsonantManner("affricate"), ConsonantPlace("dental"), True),
        Consonant("Ts", ConsonantManner("affricate"), ConsonantPlace("alveolar-central"), False),
        Consonant("dz", ConsonantManner("affricate"), ConsonantPlace("alveolar-central"), True),
        Consonant("tɬ", ConsonantManner("affricate"), ConsonantPlace("alveolar-lateral"), False),
        Consonant("dɮ", ConsonantManner("affricate"), ConsonantPlace("alveolar-lateral"), True),
        Consonant("t̪ʂ", ConsonantManner("affricate"), ConsonantPlace("retroflex"), False),
        Consonant("d̪ʐ", ConsonantManner("affricate"), ConsonantPlace("retroflex"), True),
        Consonant("ʧ", ConsonantManner("affricate"), ConsonantPlace("palatal"), False),
        Consonant("ʤ", ConsonantManner("affricate"), ConsonantPlace("palatal"), True),
        Consonant("kx", ConsonantManner("affricate"), ConsonantPlace("velar"), False),
        Consonant("gɣ", ConsonantManner("affricate"), ConsonantPlace("velar"), True),
        Consonant("qχ", ConsonantManner("affricate"), ConsonantPlace("uvular"), False),
        Consonant("ɢʁ", ConsonantManner("affricate"), ConsonantPlace("uvular"), True),
        # Resonants > Nasals
        Consonant("m̥", ConsonantManner("nasal"), ConsonantPlace("labial"), False),
        Consonant("m", ConsonantManner("nasal"), ConsonantPlace("labial"), True),
        Consonant("n̥", ConsonantManner("nasal"), ConsonantPlace("alveolar-central"), False),
        Consonant("n", ConsonantManner("nasal"), ConsonantPlace("alveolar-central"), True),
        Consonant("ɳ̊", ConsonantManner("nasal"), ConsonantPlace("retroflex"), False),
        Consonant("ɳ", ConsonantManner("nasal"), ConsonantPlace("retroflex"), True),
        Consonant("ɲ̊", ConsonantManner("nasal"), ConsonantPlace("palatal"), False),
        Consonant("ɲ", ConsonantManner("nasal"), ConsonantPlace("palatal"), True),
        Consonant("ŋ̊", ConsonantManner("nasal"), ConsonantPlace("velar"), False),
        Consonant("ŋ", ConsonantManner("nasal"), ConsonantPlace("velar"), True),
        Consonant("ɴ", ConsonantManner("nasal"), ConsonantPlace("uvular"), True),
        # Resonants > Liquids
        Consonant("ɾ̥", ConsonantManner("liquid"), ConsonantPlace("alveolar-central"), False),
        Consonant("ɾ", ConsonantManner("liquid"), ConsonantPlace("alveolar-central"), True),
        Consonant("l", ConsonantManner("liquid"), ConsonantPlace("alveolar-lateral"), True),
        Consonant("ɻ", ConsonantManner("liquid"), ConsonantPlace("retroflex"), True),
        Consonant("j", ConsonantManner("liquid"), ConsonantPlace("post-alveolar"), True),
        Consonant("w", ConsonantManner("liquid"), ConsonantPlace("velar"), True),
        Consonant("ʀ̥", ConsonantManner("liquid"), ConsonantPlace("uvular"), False),
        Consonant("ʀ", ConsonantManner("liquid"), ConsonantPlace("uvular"), True),
    ]
    # fmt: on


def get_consonant(symbol: str) -> Optional[Consonant]:
    consonants = get_consonants()
    symbols = [consonant.symbol for consonant in consonants]
    try:
        index = symbols.index(symbol)
        return consonants[index]
    except ValueError:
        return None
