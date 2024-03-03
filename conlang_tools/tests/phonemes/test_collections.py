from typing import Any
from conlang_tools.phonemes.consonants import (
    Consonant,
    ConsonantManner,
    ConsonantPlace,
)
from conlang_tools.phonemes.vowels import (
    Vowel,
    VowelLocation,
    VowelOpenness,
)
from conlang_tools.phonemes.collections import (
    find_consonant,
    find_similar_consonant,
    find_vowel,
    find_backward_vowel,
    find_forward_vowel,
    find_higher_vowel,
    find_lower_vowel,
    find_similar_vowel,
    get_consonants,
    get_consonant,
    get_phonemes,
    get_phoneme,
    get_vowels,
    get_vowel,
)


class TestFindConsonant:
    def test_find_consonant(self):
        p = find_consonant(manner="stop", place="labial", voiced=False)
        ng = find_consonant(manner="nasal", place="velar", voiced=True)
        nope = find_consonant(manner="stop", place="pharyngeal", voiced=True)

        assert p.symbol == "p"
        assert ng.symbol == "ŋ"
        assert nope is None


class TestFindSimilarConsonant:
    def test_find_similar_consonant(self):
        p = get_consonant("p")
        b = find_similar_consonant(p, voiced=True)
        t = find_similar_consonant(p, place="alveolar-central")
        f = find_similar_consonant(p, manner="fricative")
        nope = find_similar_consonant(p, manner="liquid")

        assert b.symbol == "b"
        assert t.symbol == "t"
        assert f.symbol == "f"
        assert nope is None


class TestGetConsonants:
    def test_get_vowels(self):
        consonants = get_consonants()
        assert len(consonants) == 72
        assert all(isinstance(consonant, Consonant) for consonant in consonants)


class TestGetConsonant:
    @staticmethod
    def isp(candidate: Any):
        assert isinstance(candidate, Consonant)
        assert candidate.symbol == "p"
        assert candidate.manner == "stop"
        assert isinstance(candidate.manner, ConsonantManner)
        assert candidate.place == "labial"
        assert isinstance(candidate.place, ConsonantPlace)
        assert candidate.voiced is False
        assert candidate.category == "obstruent"

    def test_get_consonant(self):
        TestGetConsonant.isp(get_consonant("p"))

    def test_returns_none_if_not_found(self):
        assert get_consonant("@") is None


class TestGetPhonemes:
    def test_get_phonemes(self):
        phonemes = get_phonemes()
        assert len(phonemes) == 138
        assert all(isinstance(p, Consonant) or isinstance(p, Vowel) for p in phonemes)


class TestGetPhoneme:
    def test_get_phoneme_consonant(self):
        TestGetConsonant.isp(get_phoneme("p"))

    def test_get_phoneme_vowel(self):
        TestGetVowel.isi(get_phoneme("i"))

    def test_returns_none_if_not_found(self):
        assert get_phoneme("@") is None


class TestFindVowel:
    def test_find_vowel(self):
        # fmt: off
        a = find_vowel(openness="open", location="front", rounded=False, long=False)
        e = find_vowel(openness="close-mid", location="front", rounded=False, long=False)
        i = find_vowel(openness="close", location="front", rounded=False, long=False)
        o = find_vowel(openness="close-mid", location="back", rounded=True, long=False)
        u = find_vowel(openness="close", location="back", rounded=True, long=False)
        long_a = find_vowel(openness="open", location="front", rounded=False, long=True)
        nope = find_vowel(openness="near-close", location="central", rounded=True, long=False)
        # fmt: on

        assert a.symbol == "a"
        assert e.symbol == "e"
        assert i.symbol == "i"
        assert o.symbol == "o"
        assert u.symbol == "u"
        assert long_a.symbol == "a:"
        assert nope is None


class TestFindSimilarVowel:
    def test_find_similar_vowel(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        w = find_similar_vowel(i, location="back")
        u = find_similar_vowel(i, location="back", rounded=True)
        a = find_similar_vowel(i, openness="open")
        y = find_similar_vowel(i, rounded=True)
        long_i = find_similar_vowel(i, long=True)

        umla = Vowel("ä", VowelOpenness("open"), VowelLocation("central"), False, False)
        nope = find_similar_vowel(umla, rounded=True)

        assert w.symbol == "ɯ"
        assert u.symbol == "u"
        assert a.symbol == "a"
        assert y.symbol == "y"
        assert long_i.symbol == "i:"
        assert nope is None


class TestFindHigherVowel:
    def test_find_higher_vowel(self):
        a = Vowel("a", VowelOpenness("open"), VowelLocation("front"), False, False)
        actual = find_higher_vowel(a)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "æ"

    def test_find_higher_vowel_no_higher(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_higher_vowel(i)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "i"

    def test_find_higher_vowel_within_set(self):
        a = Vowel("a", VowelOpenness("open"), VowelLocation("front"), False, False)
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_higher_vowel(a, [a, i])
        assert isinstance(actual, Vowel)
        assert actual.symbol == "i"


class TestFindLowerVowel:
    def test_find_lower_vowel(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_lower_vowel(i)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "ɪ"

    def test_find_lower_vowel_no_lower(self):
        a = Vowel("a", VowelOpenness("open"), VowelLocation("front"), False, False)
        actual = find_lower_vowel(a)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "a"

    def test_find_lower_vowel_within_set(self):
        a = Vowel("a", VowelOpenness("open"), VowelLocation("front"), False, False)
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_lower_vowel(i, [a, i])
        assert isinstance(actual, Vowel)
        assert actual.symbol == "a"


class TestFindForwardVowel:
    def test_find_forward_vowel(self):
        w = Vowel("ɯ", VowelOpenness("close"), VowelLocation("back"), False, False)
        actual = find_forward_vowel(w)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "ɨ"

    def test_find_forward_vowel_no_forward(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_forward_vowel(i)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "i"

    def test_find_forward_vowel_within_set(self):
        w = Vowel("ɯ", VowelOpenness("close"), VowelLocation("back"), False, False)
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_forward_vowel(w, [w, i])
        assert isinstance(actual, Vowel)
        assert actual.symbol == "i"


class TestFindBackwardVowel:
    def test_find_backward_vowel(self):
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_backward_vowel(i)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "ɨ"

    def test_find_backward_vowel_no_forward(self):
        u = Vowel("u", VowelOpenness("close"), VowelLocation("back"), True, False)
        actual = find_backward_vowel(u)
        assert isinstance(actual, Vowel)
        assert actual.symbol == "u"

    def test_find_backward_vowel_within_set(self):
        w = Vowel("ɯ", VowelOpenness("close"), VowelLocation("back"), False, False)
        i = Vowel("i", VowelOpenness("close"), VowelLocation("front"), False, False)
        actual = find_backward_vowel(i, [w, i])
        assert isinstance(actual, Vowel)
        assert actual.symbol == "ɯ"


class TestGetVowels:
    def test_get_vowels(self):
        vowels = get_vowels()
        assert len(vowels) == 66
        assert all(isinstance(vowel, Vowel) for vowel in vowels)


class TestGetVowel:
    @staticmethod
    def isi(candidate: Any):
        assert isinstance(candidate, Vowel)
        assert candidate.symbol == "i"
        assert candidate.openness == "close"
        assert isinstance(candidate.openness, VowelOpenness)
        assert candidate.location == "front"
        assert isinstance(candidate.location, VowelLocation)
        assert candidate.rounded is False

    def test_get_vowel(self):
        TestGetVowel.isi(get_vowel("i"))

    def test_returns_none_if_not_found(self):
        assert get_vowel("@") is None
