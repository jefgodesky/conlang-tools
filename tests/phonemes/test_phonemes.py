from phonemes.consonants import Consonant
from phonemes.vowels import Vowel
from tests.phonemes.test_consonant import TestGetConsonant
from tests.phonemes.test_vowel import TestGetVowel
from phonemes.phonemes import get_phonemes, get_phoneme


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
