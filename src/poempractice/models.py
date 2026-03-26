from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvaluationConfig:
    """Configuration values for validating and scoring a user line."""

    min_words: int = 3
    syllable_tolerance: int = 1
    rhyme_mode: str = "strict"
    ignore_case: bool = True
    ignore_punctuation: bool = True


@dataclass(frozen=True)
class LineAnalysis:
    """Computed metrics for a single line."""

    original_text: str
    normalized_words: list[str]
    last_word: str
    syllables: int
    unknown_words: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RhymeAnalysis:
    """Result of checking whether two words rhyme."""

    mode: str
    match: bool
    details: str


@dataclass(frozen=True)
class SyllableMatch:
    """Syllable comparison between prompt and user lines."""

    tolerance: int
    difference: int
    passed: bool


@dataclass(frozen=True)
class ScoreBreakdown:
    rhyme: int
    syllables: int
    bonus_exact_syllables: int = 0

    @property
    def total(self) -> int:
        return self.rhyme + self.syllables + self.bonus_exact_syllables


@dataclass(frozen=True)
class EvaluationResult:
    valid: bool
    errors: list[str]
    prompt: LineAnalysis | None
    user: LineAnalysis | None
    rhyme: RhymeAnalysis | None
    syllable_match: SyllableMatch | None
    score: ScoreBreakdown
    feedback: list[str]
