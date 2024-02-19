from typing import List, Optional, Union
from phonemes.consonants import Consonant, get_consonants, get_consonant
from phonemes.vowels import Vowel, get_vowels, get_vowel


def get_phonemes() -> List[Union[Consonant, Vowel]]:
    return get_consonants() + get_vowels()


def get_phoneme(symbol: str) -> Optional[Union[Consonant, Vowel]]:
    consonant = get_consonant(symbol)
    if consonant is not None:
        return consonant

    return get_vowel(symbol)
