from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Phoneme:
    symbol: str

    def __repr__(self):
        return f"[{self.symbol}]"

    def __hash__(self):
        return hash(self.symbol)
