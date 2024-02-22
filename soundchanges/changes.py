from typing import Callable, Dict, List, Optional, Tuple
import random
from language.classes import Language
from phonemes.consonants import Consonant, find_similar_consonant, get_consonant
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
        for si, syllable in enumerate(root.syllables):
            for pi, phoneme in enumerate(syllable.phonemes):
                if evaluator(root, si, pi, phoneme):
                    replace(root, si, pi, transformer(root, si, pi, phoneme))
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
    root: Root, si: int, pi: int, replacements: List[Consonant | Vowel]
) -> None:
    before = root.syllables[si].phonemes[:pi]
    after = root.syllables[si].phonemes[pi + 1 :]
    root.syllables[si].phonemes = before + replacements + after


def devoicing(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Devoicing:** Voiced consonants became voiceless "
        "at the end of words or next to voiceless consonants."
    )

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        is_consonant = isinstance(phoneme, Consonant)
        if not is_consonant or phoneme.voiced is False:
            return False

        following = root.following(si, pi)
        voiceless_neighbors = [
            isinstance(n, Consonant) and not n.voiced for n in root.neighbors(si, pi)
        ]
        return any(voiceless_neighbors) or following is None

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        return [find_similar_consonant(phoneme, voiced=False)]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def devoicing_assimilation(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Devoicing Assimilation:** Voiced consonants became voiceless "
        "when they occurred next to voiceless consonants."
    )

    consonants, _ = lang.take_inventory()

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if not isinstance(phoneme, Consonant) or phoneme.voiced is False:
            return False
        neighbors = root.neighbors(si, pi)
        voiceless = [isinstance(n, Consonant) and n.voiced is False for n in neighbors]
        return any(voiceless)

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        repl = find_similar_consonant(phoneme, voiced=False)
        return [repl if repl is not None and repl in consonants else phoneme]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def phonetic_erosion(lang: Language) -> Tuple[str, List[str]]:
    return apply_random_change(
        lang,
        {
            "coda_stops": (4, erosion_coda_stops_followed_by_consonant),
            "h_between_vowels": (5, erosion_h_between_vowels),
            "ui_becomes_jw_vowel_pair": (2, erosion_ui_becomes_jw_vowel_pair),
            "voiceless_obstruents": (1, erosion_voiceless_obstruents),
            "word_final_diphthongs": (1, erosion_word_final_diphthongs),
            "word_final_short_vowels": (3, erosion_word_final_short_vowels),
            "word_final_shortening": (3, erosion_word_final_shortening),
            "word_final_voiced_consonants": (2, erosion_word_final_voiced_consonants),
        },
    )


def erosion_coda_stops_followed_by_consonant(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Coda stops were dropped when they were followed "
        "by a consonant."
    )

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        is_consonant = isinstance(phoneme, Consonant)
        is_stop = is_consonant and phoneme.manner == "stop"
        if not is_stop or pi < len(root.syllables[si].phonemes) - 1:
            return False

        following = root.following(si, pi)
        return isinstance(following, Consonant)

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        return []

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def erosion_voiceless_obstruents(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Vowels were dropped between voiceless obstruents "
        "in unstressed syllables."
    )

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        is_vowel = isinstance(phoneme, Vowel)
        is_unstressed = root.stresses(si) is False
        if not is_vowel or not is_unstressed:
            return False

        return all(
            [
                isinstance(n, Consonant)
                and n.category == "obstruent"
                and n.voiced is False
                for n in root.neighbors(si, pi)
            ]
        )

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        return []

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def erosion_h_between_vowels(lang: Language) -> Tuple[str, List[str]]:
    description = "**Phonetic Erosion:** /h/ was dropped between vowels."

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if phoneme.symbol != "h":
            return False

        neighbors = root.neighbors(si, pi)
        return all([isinstance(n, Vowel) for n in neighbors])

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        return []

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def erosion_ui_becomes_jw_vowel_pair(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** /i/ became /j/ and /u/ became /w/ "
        "when followed by another vowel."
    )

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if phoneme.symbol != "i" and phoneme.symbol != "u":
            return False

        following = root.following(si, pi)
        return isinstance(following, Vowel)

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        symbol = "j" if phoneme.symbol == "i" else "w"
        return [get_consonant(symbol)]

    new_words = apply_change(lang, evaluator, transformer)
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


def erosion_word_final_voiced_consonants(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Phonetic Erosion:** Voiced consonants at the end of words "
        "became voiceless."
    )

    new_words: List[str] = []
    for original in lang.words:
        root = Root(original)
        last = root.phoneme_index[-1]
        if isinstance(last[2], Consonant) and last[2].voiced is True:
            voiceless = find_similar_consonant(last[2], voiced=False)
            root.syllables[-1].phonemes[-1] = voiceless
        root.rebuild()
        new_words.append(root.ipa)

    return description, new_words


def labial_assimilation(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Labial Assimilation:** Non-labial consonants became labial "
        "consonants when they occurred next to labial consonants."
    )

    consonants, _ = lang.take_inventory()

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if not isinstance(phoneme, Consonant) or phoneme.place == "labial":
            return False
        neighbors = root.neighbors(si, pi)
        labials = [isinstance(n, Consonant) and n.place == "labial" for n in neighbors]
        return any(labials)

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        labial = find_similar_consonant(phoneme, place="labial")
        return [labial if labial is not None and labial in consonants else phoneme]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def metathesis(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Metathesis:** Adjacent sibilant and stop consonants swapped "
        "positions in stressed syllables when they were preceded by "
        "a vowel."
    )

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if not root.stresses(si):
            return False

        this_c = isinstance(phoneme, Consonant)
        this_stop = this_c and phoneme.manner == "stop"
        this_sibilant = this_c and phoneme.is_sibilant()
        if not this_stop and not this_sibilant:
            return False

        preceding = root.preceding(si, pi)
        if not isinstance(preceding, Vowel):
            return False

        following = root.following(si, pi)
        following_c = isinstance(following, Consonant)
        following_stop = following_c and following.manner == "stop"
        follow_sibilant = following_c and following.is_sibilant()

        # If we crossed a syllable boundary, the change doesn't apply.
        if root.syllables[si].phonemes[pi + 1] != following:
            return False

        return any([this_stop and follow_sibilant, following_stop and this_sibilant])

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        first = root.syllables[si].phonemes[pi]
        second = root.syllables[si].phonemes[pi + 1]
        replace(root, si, pi + 1, [first])
        return [second]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def nasal_assimilation(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Nasal Assimilation:** Non-nasal consonants became nasal "
        "consonants when they occurred next to nasal consonants."
    )

    consonants, _ = lang.take_inventory()

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if not isinstance(phoneme, Consonant) or phoneme.place == "nasal":
            return False
        neighbors = root.neighbors(si, pi)
        nasals = [isinstance(n, Consonant) and n.manner == "nasal" for n in neighbors]
        return any(nasals)

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        nasal = find_similar_consonant(phoneme, manner="nasal")
        return [nasal if nasal is not None and nasal in consonants else phoneme]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def velar_assimilation(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Velar Assimilation:** Non-velar consonants became velar "
        "consonants when they occurred next to velar consonants."
    )

    consonants, _ = lang.take_inventory()

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if not isinstance(phoneme, Consonant) or phoneme.place == "velar":
            return False
        neighbors = root.neighbors(si, pi)
        velars = [isinstance(n, Consonant) and n.place == "velar" for n in neighbors]
        return any(velars)

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        velar = find_similar_consonant(phoneme, place="velar")
        return [velar if velar is not None and velar in consonants else phoneme]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def voicing(lang: Language) -> Tuple[str, List[str]]:
    description = "**Voicing:** Unvoiced consonants became voiced between vowels."

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        is_consonant = isinstance(phoneme, Consonant)
        if not is_consonant or phoneme.voiced is True:
            return False
        return all([isinstance(n, Vowel) for n in root.neighbors(si, pi)])

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        return [find_similar_consonant(phoneme, voiced=True)]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def voicing_assimilation(lang: Language) -> Tuple[str, List[str]]:
    description = (
        "**Voicing Assimilation:** Voiceless consonants became voiced "
        "when they occurred next to voiced consonants."
    )

    consonants, _ = lang.take_inventory()

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if not isinstance(phoneme, Consonant) or phoneme.voiced:
            return False
        neighbors = root.neighbors(si, pi)
        voiced = [isinstance(n, Consonant) and n.voiced for n in neighbors]
        return any(voiced)

    def transformer(
        root: Root, si: int, pi: int, phoneme: Consonant
    ) -> List[Consonant]:
        voiced = find_similar_consonant(phoneme, voiced=True)
        return [voiced if voiced is not None and voiced in consonants else phoneme]

    new_words = apply_change(lang, evaluator, transformer)
    return description, new_words


def apply_vowel_change(
    lang: Language, mapping: Dict[str, Vowel], affected: str, affected_keys: List[str]
) -> List[str]:
    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if affected != "all" and not root.stresses(si):
            return False
        return phoneme.symbol in affected_keys

    def transformer(root: Root, si: int, pi: int, phoneme: Consonant) -> List[Vowel]:
        return [mapping[phoneme.symbol]]

    return apply_change(lang, evaluator, transformer)


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

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        if not isinstance(phoneme, Vowel) or phoneme.symbol != "a":
            return False
        following = root.following(si, pi)
        return isinstance(following, Consonant) and following.place == "palatal"

    def transformer(root: Root, si: int, pi: int, phoneme: Consonant) -> List[Vowel]:
        return [get_vowel("æ")]

    new_words = apply_change(lang, evaluator, transformer)
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

    description = (
        f"**Vowel Splitting:** /{original_symbol}/ became /{target_symbols}/ "
        "in stressed syllables."
    )

    def evaluator(root: Root, si: int, pi: int, phoneme: Consonant | Vowel) -> bool:
        return root.stresses(si) and phoneme.symbol == original_symbol

    def transformer(root: Root, si: int, pi: int, phoneme: Consonant) -> List[Vowel]:
        return [get_vowel(character) for character in target_symbols]

    new_words = apply_change(lang, evaluator, transformer)
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
            "devoicing_assimilation": (5, devoicing_assimilation),
            "phonetic_erosion": (10, phonetic_erosion),
            "labial_assimilation": (3, labial_assimilation),
            "metathesis": (3, metathesis),
            "nasal_assimilation": (5, nasal_assimilation),
            "velar_assimilation": (4, velar_assimilation),
            "voicing": (9, voicing),
            "voicing_assimilation": (5, voicing_assimilation),
            "vowel_backing": (6, vowel_backing),
            "vowel_fronting": (6, vowel_fronting),
            "vowel_lengthening": (8, vowel_lengthening),
            "vowel_lowering": (7, vowel_lowering),
            "vowel_raising": (7, vowel_raising),
            "vowel_shortening": (8, vowel_shortening),
            "vowel_splitting": (8, vowel_splitting),
        },
    )
