from typing import Dict, List
from conlang_tools.phonemes.roots import Syllable
from conlang_tools.phonemes.consonants import Consonant
from conlang_tools.phonemes.vowels import Vowel


def get_choices(dictionary: Dict[str, int]) -> List[str]:
    return [key for key, value in dictionary.items() for _ in range(value)]


def oxford_comma(items: List[str]) -> str:
    if len(items) < 1:
        return ""
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return items[0] + " and " + items[1]
    else:
        return ", ".join(items[:-1]) + ", and " + items[-1]


def weigh_syllable(syllable: str) -> int:
    analysis = Syllable(syllable)
    return sum(
        [
            any(isinstance(p, Vowel) and p.long is True for p in analysis.phonemes),
            isinstance(analysis.phonemes[-1], Consonant),
        ]
    )


def weigh_syllables(syllables: List[str]) -> List[int]:
    return [weigh_syllable(syllable) for syllable in syllables]
