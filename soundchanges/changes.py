from typing import Callable, Dict, List, Optional, Tuple
import random
from language.classes import Language
from phonemes.consonants import Consonant
from phonemes.vowels import get_vowel
from phonemes.roots import Root
from phonemes.vowels import Vowel, find_similar_vowel
from utils.methods import oxford_comma, get_choices


SoundChangeFunction = Callable[[Language, ...], Tuple[str, List[str]]]


def describe_vowel_change(
    mapping: Dict[str, Vowel], name: str, syllables: Optional[str] = None
) -> Tuple[str, str, List[str]]:
    affected = get_affected_syllables(syllables)
    affected_keys = [key for key in mapping.keys() if key != mapping[key].symbol]
    changes = [f"/{key}/ became /{mapping[key].symbol}/" for key in affected_keys]
    title = f"**Vowel {name}:**"
    affects_desc = f"{oxford_comma(changes)} in {affected} syllables."
    no_changes = len(affected_keys) < 1
    affects = "No changes." if no_changes else affects_desc
    description = f"{title} {affects}"
    return description, affected, affected_keys


def get_affected_syllables(syllables: Optional[str] = None) -> str:
    rand_all = "all" if random.random() < 0.1 else "stressed"
    return syllables if syllables is not None else rand_all


def apply_vowel_change(
    lang: Language, mapping: Dict[str, Vowel], affected: str, affected_keys: List[str]
) -> List[str]:
    new_words: List[str] = []
    for original in lang.words:
        analysis = Root(original)
        for syllable in analysis.syllables:
            if affected == "all" or syllable.stressed or len(analysis.syllables) < 2:
                for index, phoneme in enumerate(syllable.phonemes):
                    if phoneme.symbol in affected_keys:
                        syllable.phonemes[index] = mapping[phoneme.symbol]
        analysis.rebuild()
        new_words.append(analysis.ipa)
    return new_words


def vowel_change(
    lang: Language,
    map_type: str = "height",
    syllables: Optional[str] = None,
    reverse: bool = True,
) -> Tuple[str, List[str]]:
    mapping = lang.vowel_mapping(map_type, reverse=reverse)
    height = "Lowering" if reverse is False else "Raising"
    direction = "Backing" if reverse is False else "Fronting"
    name = direction if map_type == "location" else height
    description, affected, affected_keys = describe_vowel_change(
        mapping, name, syllables
    )
    new_words = apply_vowel_change(lang, mapping, affected, affected_keys)
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


def vowel_lengthening(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    _, vowels = lang.take_inventory()
    mapping = {v.symbol: find_similar_vowel(v, long=True) for v in vowels}
    description, affected, affected_keys = describe_vowel_change(
        mapping, "Lengthening", syllables
    )
    new_words = apply_vowel_change(lang, mapping, affected, affected_keys)
    return description, new_words


def vowel_shortening(
    lang: Language, syllables: Optional[str] = None
) -> Tuple[str, List[str]]:
    _, vowels = lang.take_inventory()
    mapping = {v.symbol: find_similar_vowel(v, long=False) for v in vowels}
    description, affected, affected_keys = describe_vowel_change(
        mapping, "Shortening", syllables
    )
    new_words = apply_vowel_change(lang, mapping, affected, affected_keys)
    return description, new_words


def vowel_splitting(lang: Language) -> Tuple[str, List[str]]:
    return apply_random_change(
        lang,
        {
            "palatalization": (1, vowel_splitting_palatalization),
            "diphthongization": (3, vowel_splitting_stress_diphthongization),
        },
    )


def vowel_splitting_palatalization(lang: Language) -> Tuple[str, List[str]]:
    desc_title = "**Vowel Splitting:** "
    desc_changes = "/a/ became /æ/ when followed by a palatal consonant."
    description = desc_title + desc_changes

    ae = get_vowel("æ")
    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for item in root.phoneme_index:
            is_a = item[2].symbol == "a"
            following = root.following(item[0], item[1])
            following_consonant = isinstance(following, Consonant)
            following_palatal = following_consonant and following.place == "palatal"
            if is_a and following_palatal:
                root.syllables[item[0]].phonemes[item[1]] = ae
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def vowel_splitting_stress_diphthongization(
    lang: Language, original: Optional[str] = None, target: Optional[str] = None
) -> Tuple[str, List[str]]:
    options = {
        "a": ["ai", "au"],
        "e": ["ei"],
        "i": ["ie", "ia"],
        "o": ["ou"],
        "u": ["ue", "uo"],
    }
    original_symbol = (
        original if original is not None else random.choice(list(options.keys()))
    )
    target_symbols = (
        target
        if target is not None and target in options[original_symbol]
        else random.choice(options[original_symbol])
    )
    replacements = [get_vowel(character) for character in target_symbols]

    desc_title = "**Vowel Splitting:** "
    desc_changes = (
        f"/{original_symbol}/ became /{target_symbols}/ in stressed syllables."
    )
    description = desc_title + desc_changes

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable in root.syllables:
            if syllable.stressed:
                for index, phoneme in enumerate(syllable.phonemes):
                    if phoneme.symbol == original_symbol:
                        before = syllable.phonemes[:index]
                        after = syllable.phonemes[index + 1 :]
                        syllable.phonemes = before + replacements + after
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def apply_random_change(
    lang: Language, choices: Dict[str, Tuple[int, SoundChangeFunction]]
) -> Tuple[str, List[str]]:
    weighted = get_choices({key: wgt for key, (wgt, _) in choices.items()})
    chosen = random.choice(weighted)
    if chosen in choices:
        _, change_fn = choices[chosen]
        return change_fn(lang)
    else:
        return "No change.", lang.words


def change(lang: Language) -> Tuple[str, List[str]]:
    return apply_random_change(
        lang,
        {
            "vowel_backing": (6, vowel_backing),
            "vowel_fronting": (6, vowel_fronting),
            "vowel_lengthening": (8, vowel_lengthening),
            "vowel_lowering": (7, vowel_lowering),
            "vowel_raising": (7, vowel_raising),
            "vowel_shortening": (8, vowel_shortening),
            "vowel_splitting": (8, vowel_splitting),
        },
    )
