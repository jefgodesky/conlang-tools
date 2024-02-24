from conlang_tools.phonemes.consonants import Consonant
from conlang_tools.phonemes.vowels import Vowel
from conlang_tools.tests.phonemes.test_consonant import TestGetConsonant
from conlang_tools.tests.phonemes.test_vowel import TestGetVowel
from conlang_tools.phonemes.phonemes import get_phonemes, get_phoneme


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
