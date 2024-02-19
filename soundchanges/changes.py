from typing import List, Optional, Tuple
import random
from language.classes import Language
from phonemes.roots import Root
from utils.methods import oxford_comma, get_choices


def get_affected_syllables(syllables: Optional[str] = None) -> str:
    rand_all = "all" if random.random() < 0.1 else "stressed"
    return syllables if syllables is not None else rand_all


def vowel_change(
    lang: Language,
    map_type: str = "height",
    syllables: Optional[str] = None,
    reverse: bool = True,
) -> Tuple[str, List[str]]:
    affected = get_affected_syllables(syllables)
    mapping = lang.vowel_mapping(map_type, reverse=reverse)
    affected_keys = [key for key in mapping.keys() if key != mapping[key].symbol]
    changes = [f"/{key}/ became /{mapping[key].symbol}/" for key in affected_keys]
    height_direction = "Lowering" if reverse is False else "Raising"
    loc_direction = "Backing" if reverse is False else "Fronting"
    direction = loc_direction if map_type == "location" else height_direction
    title = f"**Vowel {direction}:**"
    affects_desc = f"{oxford_comma(changes)} in {affected} syllables."
    no_changes = len(affected_keys) < 1
    affects = "No changes." if no_changes else affects_desc
    description = f"{title} {affects}"

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


def vowel_lowering(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    return vowel_change(lang, "height", syllables, reverse=False)


def vowel_raising(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    return vowel_change(lang, "height", syllables)


def vowel_fronting(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    return vowel_change(lang, "location", syllables)


def vowel_backing(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    return vowel_change(lang, "location", syllables, reverse=False)


def change(lang: Language) -> Tuple[str, List[str]]:
    sound_changes = {
        "vowel_backing": (6, vowel_backing),
        "vowel_fronting": (6, vowel_fronting),
        "vowel_lowering": (7, vowel_lowering),
        "vowel_raising": (7, vowel_raising),
    }

    choices = get_choices({key: wgt for key, (wgt, _) in sound_changes.items()})
    sound_change = random.choice(choices)
    if sound_change in sound_changes:
        _, change_fn = sound_changes[sound_change]
        return change_fn(lang)
    else:
        return "No change.", lang.words
