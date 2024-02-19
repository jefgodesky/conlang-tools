from typing import List, Optional, Tuple
import random
from language.classes import Language
from phonemes.roots import Root
from utils.methods import oxford_comma


def vowel_raise(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    rand_all = "all" if random.random() < 0.1 else "stressed"
    affected = syllables if syllables is not None else rand_all
    mapping = lang.vowel_height_mapping()
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
