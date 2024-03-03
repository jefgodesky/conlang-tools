from typing import Callable, List, Optional
from conlang_tools.phonemes.phonemes import Phoneme
from conlang_tools.phonemes.consonants import (
    Consonant,
    ConsonantManner,
    ConsonantMannerTypes,
    ConsonantPlace,
    ConsonantPlaceTypes,
)
from conlang_tools.phonemes.vowels import (
    Vowel,
    VowelLocation,
    VowelLocationTypes,
    VowelOpenness,
    VowelOpennessTypes,
)


def get_consonants() -> List[Consonant]:
    # fmt: off
    return [
        # Obstruents > Stops
        Consonant("p", ConsonantManner("stop"), ConsonantPlace("labial"), False),
        Consonant("b", ConsonantManner("stop"), ConsonantPlace("labial"), True),
        Consonant("t̼", ConsonantManner("stop"), ConsonantPlace("dental"), False),
        Consonant("d̼", ConsonantManner("stop"), ConsonantPlace("dental"), True),
        Consonant("t", ConsonantManner("stop"), ConsonantPlace("alveolar-central"), False),
        Consonant("d", ConsonantManner("stop"), ConsonantPlace("alveolar-central"), True),
        Consonant("ʈ", ConsonantManner("stop"), ConsonantPlace("retroflex"), False),
        Consonant("ɖ", ConsonantManner("stop"), ConsonantPlace("retroflex"), True),
        Consonant("c", ConsonantManner("stop"), ConsonantPlace("palatal"), False),
        Consonant("ɟ", ConsonantManner("stop"), ConsonantPlace("palatal"), True),
        Consonant("k", ConsonantManner("stop"), ConsonantPlace("velar"), False),
        Consonant("g", ConsonantManner("stop"), ConsonantPlace("velar"), True),
        Consonant("q", ConsonantManner("stop"), ConsonantPlace("uvular"), False),
        Consonant("ɢ", ConsonantManner("stop"), ConsonantPlace("uvular"), True),
        Consonant("ʔ", ConsonantManner("stop"), ConsonantPlace("glottal"), False),
        # Obstruents > Fricatives
        Consonant("f", ConsonantManner("fricative"), ConsonantPlace("labial"), False),
        Consonant("v", ConsonantManner("fricative"), ConsonantPlace("labial"), True),
        Consonant("θ", ConsonantManner("fricative"), ConsonantPlace("dental"), False),
        Consonant("ð", ConsonantManner("fricative"), ConsonantPlace("dental"), True),
        Consonant("s", ConsonantManner("fricative"), ConsonantPlace("alveolar-central"), False),
        Consonant("z", ConsonantManner("fricative"), ConsonantPlace("alveolar-central"), True),
        Consonant("ɬ", ConsonantManner("fricative"), ConsonantPlace("alveolar-lateral"), False),
        Consonant("ɮ", ConsonantManner("fricative"), ConsonantPlace("alveolar-lateral"), True),
        Consonant("ʂ", ConsonantManner("fricative"), ConsonantPlace("retroflex"), False),
        Consonant("ʐ", ConsonantManner("fricative"), ConsonantPlace("retroflex"), True),
        Consonant("ç", ConsonantManner("fricative"), ConsonantPlace("palatal"), False),
        Consonant("ʝ", ConsonantManner("fricative"), ConsonantPlace("palatal"), True),
        Consonant("ʃ", ConsonantManner("fricative"), ConsonantPlace("post-alveolar"), False),
        Consonant("ʒ", ConsonantManner("fricative"), ConsonantPlace("post-alveolar"), True),
        Consonant("x", ConsonantManner("fricative"), ConsonantPlace("velar"), False),
        Consonant("ɣ", ConsonantManner("fricative"), ConsonantPlace("velar"), True),
        Consonant("χ", ConsonantManner("fricative"), ConsonantPlace("uvular"), False),
        Consonant("ʁ", ConsonantManner("fricative"), ConsonantPlace("uvular"), True),
        Consonant("ħ", ConsonantManner("fricative"), ConsonantPlace("pharyngeal"), False),
        Consonant("ʕ", ConsonantManner("fricative"), ConsonantPlace("pharyngeal"), True),
        Consonant("h", ConsonantManner("fricative"), ConsonantPlace("glottal"), False),
        Consonant("ɦ", ConsonantManner("fricative"), ConsonantPlace("glottal"), True),
        # Obstruents > Affricates
        Consonant("pf", ConsonantManner("affricate"), ConsonantPlace("labial"), False),
        Consonant("bv", ConsonantManner("affricate"), ConsonantPlace("labial"), True),
        Consonant("t̪θ", ConsonantManner("affricate"), ConsonantPlace("dental"), False),
        Consonant("d̪ð", ConsonantManner("affricate"), ConsonantPlace("dental"), True),
        Consonant("Ts", ConsonantManner("affricate"), ConsonantPlace("alveolar-central"), False),
        Consonant("dz", ConsonantManner("affricate"), ConsonantPlace("alveolar-central"), True),
        Consonant("tɬ", ConsonantManner("affricate"), ConsonantPlace("alveolar-lateral"), False),
        Consonant("dɮ", ConsonantManner("affricate"), ConsonantPlace("alveolar-lateral"), True),
        Consonant("t̪ʂ", ConsonantManner("affricate"), ConsonantPlace("retroflex"), False),
        Consonant("d̪ʐ", ConsonantManner("affricate"), ConsonantPlace("retroflex"), True),
        Consonant("ʧ", ConsonantManner("affricate"), ConsonantPlace("palatal"), False),
        Consonant("ʤ", ConsonantManner("affricate"), ConsonantPlace("palatal"), True),
        Consonant("kx", ConsonantManner("affricate"), ConsonantPlace("velar"), False),
        Consonant("gɣ", ConsonantManner("affricate"), ConsonantPlace("velar"), True),
        Consonant("qχ", ConsonantManner("affricate"), ConsonantPlace("uvular"), False),
        Consonant("ɢʁ", ConsonantManner("affricate"), ConsonantPlace("uvular"), True),
        # Resonants > Nasals
        Consonant("m̥", ConsonantManner("nasal"), ConsonantPlace("labial"), False),
        Consonant("m", ConsonantManner("nasal"), ConsonantPlace("labial"), True),
        Consonant("n̥", ConsonantManner("nasal"), ConsonantPlace("alveolar-central"), False),
        Consonant("n", ConsonantManner("nasal"), ConsonantPlace("alveolar-central"), True),
        Consonant("ɳ̊", ConsonantManner("nasal"), ConsonantPlace("retroflex"), False),
        Consonant("ɳ", ConsonantManner("nasal"), ConsonantPlace("retroflex"), True),
        Consonant("ɲ̊", ConsonantManner("nasal"), ConsonantPlace("palatal"), False),
        Consonant("ɲ", ConsonantManner("nasal"), ConsonantPlace("palatal"), True),
        Consonant("ŋ̊", ConsonantManner("nasal"), ConsonantPlace("velar"), False),
        Consonant("ŋ", ConsonantManner("nasal"), ConsonantPlace("velar"), True),
        Consonant("ɴ", ConsonantManner("nasal"), ConsonantPlace("uvular"), True),
        # Resonants > Liquids
        Consonant("ɾ̥", ConsonantManner("liquid"), ConsonantPlace("alveolar-central"), False),
        Consonant("ɾ", ConsonantManner("liquid"), ConsonantPlace("alveolar-central"), True),
        Consonant("l", ConsonantManner("liquid"), ConsonantPlace("alveolar-lateral"), True),
        Consonant("ɻ", ConsonantManner("liquid"), ConsonantPlace("retroflex"), True),
        Consonant("j", ConsonantManner("liquid"), ConsonantPlace("post-alveolar"), True),
        Consonant("w", ConsonantManner("liquid"), ConsonantPlace("velar"), True),
        Consonant("ʀ̥", ConsonantManner("liquid"), ConsonantPlace("uvular"), False),
        Consonant("ʀ", ConsonantManner("liquid"), ConsonantPlace("uvular"), True),
    ]
    # fmt: on


def get_consonant(symbol: str) -> Optional[Consonant]:
    consonants = get_consonants()
    symbols = [consonant.symbol for consonant in consonants]
    try:
        index = symbols.index(symbol)
        return consonants[index]
    except ValueError:
        return None


def find_consonant(
    manner: ConsonantMannerTypes,
    place: ConsonantPlaceTypes,
    voiced: bool,
) -> Optional[Consonant]:
    consonants = get_consonants()
    for consonant in consonants:
        matches = [
            consonant.manner == manner,
            consonant.place == place,
            consonant.voiced == voiced,
        ]
        if all(matches):
            return consonant
    return None


def find_similar_consonant(
    consonant: Consonant,
    manner: Optional[ConsonantMannerTypes] = None,
    place: Optional[ConsonantPlaceTypes] = None,
    voiced: Optional[bool] = None,
) -> Optional[Consonant]:
    manner_arg = manner if manner is not None else consonant.manner.value
    place_arg = place if place is not None else consonant.place.value
    voiced_arg = voiced if voiced is not None else consonant.voiced
    return find_consonant(
        manner=manner_arg,
        place=place_arg,
        voiced=voiced_arg,
    )


def get_vowels() -> List[Vowel]:
    # fmt: off
    short = [
        Vowel("i", VowelOpenness("close"), VowelLocation("front"), False),
        Vowel("y", VowelOpenness("close"), VowelLocation("front"), True),
        Vowel("ɨ", VowelOpenness("close"), VowelLocation("central"), False),
        Vowel("ʉ", VowelOpenness("close"), VowelLocation("central"), True),
        Vowel("ɯ", VowelOpenness("close"), VowelLocation("back"), False),
        Vowel("u", VowelOpenness("close"), VowelLocation("back"), True),
        Vowel("ɪ", VowelOpenness("near-close"), VowelLocation("front"), False),
        Vowel("ʏ", VowelOpenness("near-close"), VowelLocation("front"), True),
        Vowel("ʊ", VowelOpenness("near-close"), VowelLocation("back"), True),
        Vowel("e", VowelOpenness("close-mid"), VowelLocation("front"), False),
        Vowel("ø", VowelOpenness("close-mid"), VowelLocation("front"), True),
        Vowel("ɘ", VowelOpenness("close-mid"), VowelLocation("central"), False),
        Vowel("ɵ", VowelOpenness("close-mid"), VowelLocation("central"), True),
        Vowel("ɤ", VowelOpenness("close-mid"), VowelLocation("back"), False),
        Vowel("o", VowelOpenness("close-mid"), VowelLocation("back"), True),
        Vowel("e̞", VowelOpenness("mid"), VowelLocation("front"), False),
        Vowel("ø̞̞", VowelOpenness("mid"), VowelLocation("front"), True),
        Vowel("ə", VowelOpenness("mid"), VowelLocation("front"), False),
        Vowel("ɤ̞", VowelOpenness("mid"), VowelLocation("back"), False),
        Vowel("o̞", VowelOpenness("mid"), VowelLocation("back"), True),
        Vowel("ɛ", VowelOpenness("open-mid"), VowelLocation("front"), False),
        Vowel("œ", VowelOpenness("open-mid"), VowelLocation("front"), True),
        Vowel("ɜ", VowelOpenness("open-mid"), VowelLocation("central"), False),
        Vowel("ɞ", VowelOpenness("open-mid"), VowelLocation("central"), True),
        Vowel("ʌ", VowelOpenness("open-mid"), VowelLocation("back"), False),
        Vowel("ɔ", VowelOpenness("open-mid"), VowelLocation("back"), True),
        Vowel("æ", VowelOpenness("near-open"), VowelLocation("front"), False),
        Vowel("ɐ", VowelOpenness("near-open"), VowelLocation("central"), False),
        Vowel("a", VowelOpenness("open"), VowelLocation("front"), False),
        Vowel("ɶ", VowelOpenness("open"), VowelLocation("front"), True),
        Vowel("ä", VowelOpenness("open"), VowelLocation("central"), False),
        Vowel("ɑ", VowelOpenness("open"), VowelLocation("back"), False),
        Vowel("ɒ", VowelOpenness("open"), VowelLocation("back"), True),
    ]
    # fmt: on

    long = [
        Vowel(v.symbol + ":", v.openness, v.location, v.rounded, long=True)
        for v in short
    ]
    return long + short


def get_vowel(symbol: str) -> Optional[Vowel]:
    vowels = get_vowels()
    symbols = [vowel.symbol for vowel in vowels]
    try:
        index = symbols.index(symbol)
        return vowels[index]
    except ValueError:
        return None


def find_vowel(
    openness: VowelOpennessTypes,
    location: VowelLocationTypes,
    rounded: bool,
    long: bool,
) -> Optional[Vowel]:
    vowels = get_vowels()
    for vowel in vowels:
        matches = [
            vowel.openness == openness,
            vowel.location == location,
            vowel.rounded == rounded,
            vowel.long == long,
        ]
        if all(matches):
            return vowel
    return None


def find_similar_vowel(
    vowel: Vowel,
    openness: Optional[VowelOpennessTypes] = None,
    location: Optional[VowelLocationTypes] = None,
    rounded: Optional[bool] = None,
    long: Optional[bool] = None,
) -> Optional[Vowel]:
    openness_arg = openness if openness is not None else vowel.openness.value
    location_arg = location if location is not None else vowel.location.value
    rounded_arg = rounded if rounded is not None else vowel.rounded
    long_arg = long if long is not None else vowel.long
    return find_vowel(
        openness=openness_arg,
        location=location_arg,
        rounded=rounded_arg,
        long=long_arg,
    )


def find_next_vowel(
    vowel: Vowel,
    fn: Callable,
    attribute: str = "openness",
    vowels: Optional[List[Vowel]] = None,
) -> Vowel:
    vowels = vowels if vowels is not None else get_vowels()
    next_vowel = None
    value = vowel.openness.value if attribute == "openness" else vowel.location.value
    while next_vowel is None:
        next_value = fn(value)
        terminus = value == next_value
        value = next_value
        next_vowel = (
            find_similar_vowel(vowel, openness=value)
            if attribute == "openness"
            else find_similar_vowel(vowel, location=value)
        )
        if next_vowel not in vowels:
            next_vowel = None
        elif terminus:
            next_vowel = vowel
    return next_vowel


def find_higher_vowel(vowel: Vowel, vowels: Optional[List[Vowel]] = None) -> Vowel:
    return find_next_vowel(vowel, VowelOpenness.higher, "openness", vowels)


def find_lower_vowel(vowel: Vowel, vowels: Optional[List[Vowel]] = None) -> Vowel:
    return find_next_vowel(vowel, VowelOpenness.lower, "openness", vowels)


def find_forward_vowel(vowel: Vowel, vowels: Optional[List[Vowel]] = None) -> Vowel:
    return find_next_vowel(vowel, VowelLocation.forward, "location", vowels)


def find_backward_vowel(vowel: Vowel, vowels: Optional[List[Vowel]] = None) -> Vowel:
    return find_next_vowel(vowel, VowelLocation.backward, "location", vowels)


def get_phonemes() -> List[Phoneme]:
    return get_consonants() + get_vowels()


def get_phoneme(symbol: str) -> Optional[Phoneme]:
    consonant = get_consonant(symbol)
    if consonant is not None:
        return consonant

    return get_vowel(symbol)
