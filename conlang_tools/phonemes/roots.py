from typing import List, Optional, Tuple
from conlang_tools.phonemes.consonants import Consonant
from conlang_tools.phonemes.vowels import Vowel
from conlang_tools.phonemes.collections import get_phonemes


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

    @property
    def nucleus_index(self) -> Optional[Tuple[int, int]]:
        start = None
        end = None
        for index in range(len(self.phonemes)):
            if isinstance(self.phonemes[index], Vowel) and start is None:
                start = index
            elif not isinstance(self.phonemes[index], Vowel) and start is not None:
                end = index - 1
        end = end if end is not None else len(self.phonemes) - 1
        return None if start is None else (start, end)

    @property
    def nucleus(self) -> Optional[str]:
        if self.nucleus_index is None:
            return None

        start, end = self.nucleus_index
        return self.unmarked[start : end + 1]

    @property
    def onset(self) -> Optional[str]:
        if self.nucleus_index is None or self.nucleus_index[0] == 0:
            return None

        return self.unmarked[: self.nucleus_index[0]]

    @property
    def coda(self) -> Optional[str]:
        last_index = len(self.phonemes) - 1
        if self.nucleus_index is None or self.nucleus_index[1] >= last_index:
            return None

        return self.unmarked[self.nucleus_index[1] + 1 :]

    def is_open(self) -> bool:
        index = self.nucleus_index
        last_index = len(self.phonemes) - 1
        return index is not None and index[1] >= last_index

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

    @property
    def phonemes(self) -> List[Consonant | Vowel]:
        return [phoneme for syllable in self.syllables for phoneme in syllable.phonemes]

    @property
    def phoneme_index(self) -> List[Tuple[int, int, Consonant | Vowel]]:
        index: List[Tuple[int, int, Consonant | Vowel]] = []
        for syllable_index, syllable in enumerate(self.syllables):
            for phoneme_index, phoneme in enumerate(syllable.phonemes):
                index.append((syllable_index, phoneme_index, phoneme))
        return index

    def stresses(self, syllable_index: int) -> bool:
        if len(self.syllables) < 2:
            return True
        return self.syllables[syllable_index].stressed

    def rebuild(self):
        for index, syllable in enumerate(self.syllables):
            if len(self.syllables) < 2:
                self.syllables[0].stressed = False

            syllable.rebuild()

            # If we end up with a syllable that's just consonants and no
            # vowels, glom it onto the syllable that occurs before it and
            # remove it from the root.

            consonants = [isinstance(p, Consonant) for p in syllable.phonemes]
            if all(consonants) and index > 0:
                prev = self.syllables[index - 1]
                prev.phonemes = prev.phonemes + syllable.phonemes
                self.syllables = self.syllables[:index] + self.syllables[index + 1 :]
                if len(self.syllables) < 2:
                    self.syllables[0].stressed = False
                prev.rebuild()

        syllables = [s.unbracketed for s in self.syllables]
        self.ipa = f"/{'.'.join(syllables)}/"

    def preceding(self, syllable: int, phoneme: int) -> Optional[Consonant | Vowel]:
        p = self.syllables[syllable].phonemes[phoneme]
        index = self.phoneme_index.index((syllable, phoneme, p))
        if index < 1:
            return None
        return self.phoneme_index[index - 1][2]

    def following(self, syllable: int, phoneme: int) -> Optional[Consonant | Vowel]:
        p = self.syllables[syllable].phonemes[phoneme]
        index = self.phoneme_index.index((syllable, phoneme, p))
        if index > len(self.phonemes) - 2:
            return None
        return self.phoneme_index[index + 1][2]

    def neighbors(
        self, syllable: int, phoneme: int
    ) -> List[Optional[Consonant | Vowel]]:
        return [
            self.preceding(syllable, phoneme),
            self.following(syllable, phoneme),
        ]
