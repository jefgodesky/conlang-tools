from typing import Callable, Dict, List, Optional, Tuple
import random
from language.classes import Language
from phonemes.consonants import Consonant, find_similar_consonant
from phonemes.vowels import get_vowel
from phonemes.roots import Root
from phonemes.vowels import Vowel, find_similar_vowel
from utils.methods import oxford_comma, get_choices


def apply_change(
    lang: Language, evaluator: Callable, transformer: Callable
) -> List[str]:
    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable_index, syllable in enumerate(root.syllables):
            for phoneme_index, phoneme in enumerate(syllable.phonemes):
                if evaluator(root, syllable_index, phoneme_index, phoneme):
                    replace(root, syllable_index, phoneme_index, transformer(phoneme))
        root.rebuild()
        new_words.append(root.ipa)
    return new_words


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


def replace(
    root: Root,
    syllable_index: int,
    phoneme_index: int,
    replacements: List[Consonant | Vowel],
) -> None:
    before = root.syllables[syllable_index].phonemes[:phoneme_index]
    after = root.syllables[syllable_index].phonemes[phoneme_index + 1 :]
    root.syllables[syllable_index].phonemes = before + replacements + after


def devoicing(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Devoicing:** Voiced consonants became voiceless "
        "at the end of words or next to voiceless consonants."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable_index, phoneme_index, phoneme in root.phoneme_index:
            p = root.syllables[syllable_index].phonemes[phoneme_index]
            if isinstance(p, Consonant) and p.voiced is True:
                following = root.following(syllable_index, phoneme_index)
                neighbors = [root.preceding(syllable_index, phoneme_index), following]
                voiceless_neighbors = [
                    isinstance(n, Consonant) and n.voiced is False for n in neighbors
                ]
                if any(voiceless_neighbors) or following is None:
                    voiceless = find_similar_consonant(p, voiced=False)
                    root.syllables[syllable_index].phonemes[phoneme_index] = voiceless
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def phonetic_erosion(lang: Language) -> Tuple[str, List[str]]:
    return apply_random_change(
        lang,
        {
            "voiceless_obstruents": (1, erosion_voiceless_obstruents),
            "h_between_vowels": (5, erosion_h_between_vowels),
            "coda_stops": (4, erosion_coda_stops_followed_by_consonant),
            "word_final_diphthongs": (1, erosion_word_final_diphthongs),
            "word_final_short_vowels": (3, erosion_word_final_short_vowels),
            "word_final_shortening": (3, erosion_word_final_shortening),
        },
    )


def erosion_coda_stops_followed_by_consonant(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Coda stops were dropped when they were followed "
        "by a consonant."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable_index, syllable in enumerate(root.syllables):
            final_index = len(syllable.phonemes) - 1
            final = syllable.phonemes[final_index]
            if isinstance(final, Consonant) and final.manner == "stop":
                followed = root.following(syllable_index, final_index)
                if isinstance(followed, Consonant):
                    replace(root, syllable_index, final_index, [])
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def erosion_voiceless_obstruents(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Vowels were dropped between voiceless obstruents "
        "in unstressed syllables."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable_index, syllable in enumerate(root.syllables):
            stressed = syllable.stressed or len(root.syllables) < 2
            if not stressed:
                for phoneme_index, phoneme in enumerate(syllable.phonemes):
                    if isinstance(phoneme, Vowel):
                        neighbors = [
                            root.preceding(syllable_index, phoneme_index),
                            root.following(syllable_index, phoneme_index),
                        ]
                        obs = [
                            isinstance(n, Consonant)
                            and n.voiced is False
                            and n.category == "obstruent"
                            for n in neighbors
                        ]
                        if all(obs):
                            replace(root, syllable_index, phoneme_index, [])
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def erosion_h_between_vowels(lang: Language) -> Tuple[str, List[str]]:
    description = "**Phonetic Erosion:** /h/ was dropped between vowels."

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable_index, syllable in enumerate(root.syllables):
            for phoneme_index, phoneme in enumerate(syllable.phonemes):
                if phoneme.symbol == "h":
                    neighbors = [
                        root.preceding(syllable_index, phoneme_index),
                        root.following(syllable_index, phoneme_index),
                    ]
                    vowels = [isinstance(n, Vowel) for n in neighbors]
                    if all(vowels):
                        replace(root, syllable_index, phoneme_index, [])
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def erosion_word_final_diphthongs(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Diphthongs that occurred at the end of "
        "a word were simplified into the long-vowel form of the first "
        "vowel in the original diphthong."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        ult = root.phoneme_index[-1]
        penult = root.phoneme_index[-2]
        if isinstance(ult[2], Vowel) and isinstance(penult[2], Vowel):
            long = find_similar_vowel(penult[2], long=True)
            replace(root, penult[0], penult[1], [long])
            replace(root, ult[0], ult[1], [])
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def erosion_word_final_short_vowels(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Short vowels that occurred as the last "
        "sound in a word were dropped."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        last = root.phoneme_index[-1]
        if isinstance(last[2], Vowel) and last[2].long is False:
            replace(root, last[0], last[1], [])
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def erosion_word_final_shortening(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Long vowels that occurred as the last "
        "sound in a word became short vowels."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        last = root.phoneme_index[-1]
        if isinstance(last[2], Vowel) and last[2].long is True:
            root.syllables[-1].phonemes[-1] = find_similar_vowel(last[2], long=False)
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def voicing(lang: Language) -> Tuple[str, List[str]]:
    description = "**Voicing:** Unvoiced consonants became voiced between vowels."

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable_index, phoneme_index, phoneme in root.phoneme_index:
            p = root.syllables[syllable_index].phonemes[phoneme_index]
            if isinstance(p, Consonant) and p.voiced is False:
                preceding = root.preceding(syllable_index, phoneme_index)
                vowel_preceding = isinstance(preceding, Vowel)
                following = root.following(syllable_index, phoneme_index)
                vowel_following = isinstance(following, Vowel)
                if vowel_preceding and vowel_following:
                    voiced = find_similar_consonant(p, voiced=True)
                    root.syllables[syllable_index].phonemes[phoneme_index] = voiced
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


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
    description = (
        "**Vowel Splitting:** /a/ became /æ/ when followed by a palatal consonant."
    )

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

    description = (
        f"**Vowel Splitting:** /{original_symbol}/ became /{target_symbols}/ "
        "in stressed syllables."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        for syllable_index, syllable in enumerate(root.syllables):
            if syllable.stressed:
                for index, phoneme in enumerate(syllable.phonemes):
                    if phoneme.symbol == original_symbol:
                        replace(root, syllable_index, index, replacements)
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def apply_random_change(
    lang: Language, choices: Dict[str, Tuple[int, Callable]]
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
            "devoicing": (10, devoicing),
            "phonetic_erosion": (10, phonetic_erosion),
            "voicing": (9, voicing),
            "vowel_backing": (6, vowel_backing),
            "vowel_fronting": (6, vowel_fronting),
            "vowel_lengthening": (8, vowel_lengthening),
            "vowel_lowering": (7, vowel_lowering),
            "vowel_raising": (7, vowel_raising),
            "vowel_shortening": (8, vowel_shortening),
            "vowel_splitting": (8, vowel_splitting),
        },
    )
