from typing import Dict, List, Literal, Optional, Tuple
import random
import yaml
from phonemes.consonants import Consonant
from phonemes.vowels import Vowel
from phonemes.roots import Syllable
from utils.methods import get_choices, weigh_syllables

# Sadly, we can't automate literal-to-list, so if you update this list, make
# sure you update Stress.types to match!
StressTypes = Literal[
    "initial", "final", "penultimate", "antepenultimate", "heavy", "random"
]
languages_directory = "languages/"


class Phonology:
    def __init__(self, stress: Optional[StressTypes] = None, openness: float = 0.5):
        self.stress = Stress(stress)
        self.openness = openness


class Phonotactics:
    def __init__(
        self,
        onset: Optional[Dict[str, int]] = None,
        nucleus: Optional[Dict[str, int]] = None,
        coda: Optional[Dict[str, int]] = None,
    ):
        self.onset = onset if onset is not None else {}
        self.nucleus = nucleus if nucleus is not None else {}
        self.coda = coda if coda is not None else {}

    def choices(self, element: str = "nucleus") -> List[str]:
        if element == "onset":
            return get_choices(self.onset)
        elif element == "coda":
            return get_choices(self.coda)
        else:
            return get_choices(self.nucleus)


class Stress:
    def __init__(self, value: Optional[StressTypes] = None):
        types = Stress.types()
        self.value = value if value is not None else types[0]
        if not Stress.isstress(self.value):
            raise TypeError(
                f"{self.value} is not a valid value for Stress. Choose one of: {', '.join(types)}."
            )

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


class Language:
    def __init__(
        self,
        phonotactics: Optional[Phonotactics] = None,
        phonology: Optional[Phonology] = None,
        words: Optional[List[str]] = None,
    ):
        self.phonotactics = phonotactics if phonotactics is not None else Phonotactics()
        self.phonology = phonology if phonology is not None else Phonology()
        self.words: List[str] = words if words is not None else []
        self.generated: List[str] = []

    def take_inventory(self) -> Tuple[List[Consonant], List[Vowel]]:
        onset = [Syllable(key) for key in self.phonotactics.onset.keys()]
        nucleus = [Syllable(key) for key in self.phonotactics.nucleus.keys()]
        coda = [Syllable(key) for key in self.phonotactics.coda.keys()]

        analyses = onset + nucleus + coda
        phonemes = [p for a in analyses for p in a.phonemes]

        consonants = [p for p in phonemes if isinstance(p, Consonant)]
        consonants = list(set(consonants))

        vowels = [p for p in phonemes if isinstance(p, Vowel)]
        vowels = list(set(vowels))

        return consonants, vowels

    def generate_syllable(self):
        onset = random.choice(self.phonotactics.choices("onset"))
        nucleus = random.choice(self.phonotactics.choices("nucleus"))
        coda = random.choice(self.phonotactics.choices("coda"))

        open_syllable = onset + nucleus
        closed_syllable = onset + nucleus + coda

        is_open = random.random() < self.phonology.openness
        return open_syllable if is_open else closed_syllable

    def apply_stress(self, syllables: List[str]):
        if len(syllables) < 2:
            return syllables

        if self.phonology.stress == "final":
            index = -1
        elif self.phonology.stress == "penultimate":
            index = -2
        elif self.phonology.stress == "antepenultimate":
            index = -3 if len(syllables) > 2 else 0
        elif self.phonology.stress == "random":
            index = random.randrange(0, len(syllables))
        elif self.phonology.stress == "heavy":
            weights = weigh_syllables(syllables)
            index = weights.index(max(weights))
        else:
            index = 0

        syllables[index] = "ˈ" + syllables[index]
        return syllables

    def generate_word(self, num_syllables: int = 1):
        syllables = [self.generate_syllable() for _ in range(num_syllables)]
        stressed = self.apply_stress(syllables)
        return f"/{'.'.join(stressed)}/"

    def generate_new_word(self, num_syllables: int = 1):
        for _ in range(10):
            word = self.generate_word(num_syllables)
            if word not in self.words and word not in self.generated:
                self.generated.append(word)
                return word
        return self.generate_new_word(num_syllables + 1)

    def generate_new_words(self, num_words: int = 1, num_syllables: int = 1):
        return [
            self.generate_new_word(num_syllables=num_syllables)
            for _ in range(num_words)
        ]

    @classmethod
    def load(cls, name: str) -> "Language":
        with open(f"{languages_directory}{name}.yaml", "r") as yaml_file:
            data = yaml.safe_load(yaml_file)
            phonotactics = Phonotactics(
                onset=data["phonotactics"]["onset"],
                nucleus=data["phonotactics"]["nucleus"],
                coda=data["phonotactics"]["coda"],
            )
            phonology = Phonology(
                stress=data["phonology"]["stress"],
                openness=data["phonology"]["openness"],
            )
            return cls(
                phonotactics=phonotactics, phonology=phonology, words=data["words"]
            )
