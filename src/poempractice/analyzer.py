from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol


class Analyzer(Protocol):
    """Interface for algorithmic language analysis.

    Swap this implementation with CMUdict or a custom NLP pipeline later.
    """

    def normalize(self, line: str) -> list[str]:
        """Return normalized word tokens for a line."""

    def syllables_for_line(self, words: list[str]) -> tuple[int, list[str]]:
        """Return total syllables and unknown words for tokens."""

    def rhymes(self, prompt_last_word: str, user_last_word: str, mode: str = "strict") -> tuple[bool, str]:
        """Return rhyme decision and human-readable details."""


@dataclass
class SimpleAnalyzer:
    """Baseline implementation so the game runs before advanced algorithms are added.

    Notes:
    - Syllables are estimated heuristically.
    - Rhyme is approximated from final vowel clusters.
    - Unknown words are never produced here; hook in dictionary lookup to enable that.
    """

    ignore_case: bool = True
    ignore_punctuation: bool = True

    _token_pattern = re.compile(r"[a-zA-Z']+")

    def normalize(self, line: str) -> list[str]:
        raw = line.lower() if self.ignore_case else line
        if self.ignore_punctuation:
            return self._token_pattern.findall(raw)
        return raw.split()

    def syllables_for_line(self, words: list[str]) -> tuple[int, list[str]]:
        return sum(_estimate_syllables(w) for w in words), []

    def rhymes(self, prompt_last_word: str, user_last_word: str, mode: str = "strict") -> tuple[bool, str]:
        if not prompt_last_word or not user_last_word:
            return False, "Missing final word in one or both lines."

        left = _rhyme_tail(prompt_last_word)
        right = _rhyme_tail(user_last_word)
        match = left == right and len(left) > 0
        if mode != "strict":
            # Placeholder so non-strict modes can be introduced without API changes.
            return match, f"Mode '{mode}' currently falls back to strict."
        return match, "Rhyme tails match." if match else f"Rhyme tails differ: '{left}' vs '{right}'."


def _estimate_syllables(word: str) -> int:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0

    groups = re.findall(r"[aeiouy]+", w)
    count = len(groups)

    if w.endswith("e") and not w.endswith(("le", "ye")) and count > 1:
        count -= 1
    return max(1, count)


def _rhyme_tail(word: str) -> str:
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return ""

    match = re.search(r"[aeiouy][a-z]*$", w)
    if match:
        return match.group(0)
    return w[-2:]
