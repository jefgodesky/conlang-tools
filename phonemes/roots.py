from typing import List
from phonemes.consonants import Consonant
from phonemes.vowels import Vowel
from phonemes.phonemes import get_phonemes


class Syllable:
    def __init__(self, ipa: str):
        self.ipa = ipa
        self.stressed = self.unbracketed.startswith("ˈ")
        self.phonemes = self.get_phonemes()

    @property
    def unbracketed(self):
        return self.ipa.strip("/[]")

    @property
    def unmarked(self):
        markings = str.maketrans("", "", "ˈ.")
        return self.unbracketed.translate(markings)

    def get_phonemes(self) -> List[Consonant | Vowel]:
        phonemes = get_phonemes()
        phonemes.sort(key=lambda p: len(p.symbol), reverse=True)
        breakdown: List[Consonant | Vowel] = []
        working = self.unmarked

        while working:
            for phoneme in phonemes:
                if working.startswith(phoneme.symbol):
                    breakdown.append(phoneme)
                    working = working[len(phoneme.symbol) :]
                    break
            else:
                raise ValueError(
                    f"Unrecognized IPA sequence at the start of: {working}"
                )

        return breakdown

    def rebuild(self):
        self.ipa = "".join([p.symbol for p in self.phonemes])
        if self.stressed:
            self.ipa = "ˈ" + self.ipa
        self.ipa = f"/{self.ipa}/"


class Root:
    def __init__(self, ipa: str):
        self.ipa = ipa
        self.syllables = [Syllable(ipa) for ipa in self.unbracketed.split(".")]

    @property
    def unbracketed(self):
        return self.ipa.strip("/[]")

    def rebuild(self):
        for syllable in self.syllables:
            syllable.rebuild()

        syllables = [s.unbracketed for s in self.syllables]
        self.ipa = f"/{'.'.join(syllables)}/"
