from typing import Dict, List, Optional, Tuple
import random
from language.classes import Language
from soundchanges.describe import oxford_comma
from phonemes.roots import Root
from phonemes.vowels import Vowel, VowelOpenness


def create_vowel_raise_mapping(lang: Language) -> Dict[str, Vowel]:
    _, vowels = lang.take_inventory()
    heights = VowelOpenness.types()
    indices = [(heights.index(v.openness.value), v) for v in vowels]
    sorted_indices = sorted(indices, key=lambda x: x[0], reverse=True)
    mapping = {}

    for i, (height, vowel) in enumerate(sorted_indices):
        if i < len(sorted_indices) - 1:
            next_highest_vowel = sorted_indices[i + 1][1]
            mapping[vowel.symbol] = next_highest_vowel
        else:
            mapping[vowel.symbol] = vowel

    return mapping


def vowel_raise(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    rand_all = "all" if random.random() < 0.1 else "stressed"
    affected = syllables if syllables is not None else rand_all
    mapping = create_vowel_raise_mapping(lang)
    affected_keys = [key for key in mapping.keys() if key != mapping[key].symbol]
    changes = [f"/{key}/ became /{mapping[key].symbol}/" for key in affected_keys]
    description = f"**Vowel Raise:** {oxford_comma(changes)} in {affected} syllables."

    new_words: List[str] = []
    for original in lang.words:
        print(original)
        analysis = Root(original)
        for syllable in analysis.syllables:
            if affected == "all" or syllable.stressed:
                for index, phoneme in enumerate(syllable.phonemes):
                    if phoneme.symbol in affected_keys:
                        syllable.phonemes[index] = mapping[phoneme.symbol]
        analysis.rebuild()
        new_words.append(analysis.ipa)

    return description, new_words
