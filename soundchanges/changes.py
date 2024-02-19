from typing import List, Optional, Tuple
import random
from language.classes import Language
from phonemes.roots import Root
from utils.methods import oxford_comma, get_choices


def vowel_raise_lower(
    lang: Language, syllables: Optional[str] = None, rise: bool = True
) -> Tuple[str, List[str]]:
    rand_all = "all" if random.random() < 0.1 else "stressed"
    affected = syllables if syllables is not None else rand_all
    mapping = lang.vowel_height_mapping(rise)
    affected_keys = [key for key in mapping.keys() if key != mapping[key].symbol]
    changes = [f"/{key}/ became /{mapping[key].symbol}/" for key in affected_keys]
    direction = "Lower" if rise is False else "Raise"
    title = f"**Vowel {direction}:**"
    description = f"{title} {oxford_comma(changes)} in {affected} syllables."

    new_words: List[str] = []
    for original in lang.words:
        analysis = Root(original)
        for syllable in analysis.syllables:
            if affected == "all" or syllable.stressed:
                for index, phoneme in enumerate(syllable.phonemes):
                    if phoneme.symbol in affected_keys:
                        syllable.phonemes[index] = mapping[phoneme.symbol]
        analysis.rebuild()
        new_words.append(analysis.ipa)

    return description, new_words


def vowel_lower(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    return vowel_raise_lower(lang, syllables, rise=False)


def vowel_raise(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    return vowel_raise_lower(lang, syllables)


def change(lang: Language) -> Tuple[str, List[str]]:
    sound_changes = {"vowel_lower": 7, "vowel_raise": 7}
    sound_change = get_choices(sound_changes)

    if sound_change == "vowel_lower":
        return vowel_lower(lang)
    elif sound_change == "vowel_raise":
        return vowel_raise(lang)
    else:
        return "No change.", lang.words
