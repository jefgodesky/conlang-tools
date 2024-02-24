from typing import List, Optional
from conlang_tools.phonemes.consonants import Consonant, get_consonants, get_consonant
from conlang_tools.phonemes.vowels import Vowel, get_vowels, get_vowel


def get_phonemes() -> List[Consonant | Vowel]:
    return get_consonants() + get_vowels()


def get_phoneme(symbol: str) -> Optional[Consonant | Vowel]:
    consonant = get_consonant(symbol)
    if consonant is not None:
        return consonant

    return get_vowel(symbol)
