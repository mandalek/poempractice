from __future__ import annotations

from poempractice.analyzer import Analyzer, SimpleAnalyzer
from poempractice.models import (
    EvaluationConfig,
    EvaluationResult,
    LineAnalysis,
    RhymeAnalysis,
    ScoreBreakdown,
    SyllableMatch,
)


def evaluate_submission(
    prompt_line: str,
    user_line: str,
    config: EvaluationConfig | None = None,
    analyzer: Analyzer | None = None,
) -> EvaluationResult:
    """Evaluate a user line against a prompt line.

    The analyzer parameter is intentionally injectable so rhyme/syllable algorithms
    can be replaced independently from game logic.
    """

    cfg = config or EvaluationConfig()
    engine = analyzer or SimpleAnalyzer(
        ignore_case=cfg.ignore_case,
        ignore_punctuation=cfg.ignore_punctuation,
    )

    prompt_words = engine.normalize(prompt_line)
    user_words = engine.normalize(user_line)

    errors: list[str] = []
    if len(user_words) < cfg.min_words:
        errors.append(f"LINE_TOO_SHORT: expected at least {cfg.min_words} words.")

    prompt_syllables, prompt_unknown = engine.syllables_for_line(prompt_words)
    user_syllables, user_unknown = engine.syllables_for_line(user_words)

    prompt_analysis = LineAnalysis(
        original_text=prompt_line,
        normalized_words=prompt_words,
        last_word=prompt_words[-1] if prompt_words else "",
        syllables=prompt_syllables,
        unknown_words=prompt_unknown,
    )
    user_analysis = LineAnalysis(
        original_text=user_line,
        normalized_words=user_words,
        last_word=user_words[-1] if user_words else "",
        syllables=user_syllables,
        unknown_words=user_unknown,
    )

    if errors:
        return EvaluationResult(
            valid=False,
            errors=errors,
            prompt=prompt_analysis,
            user=user_analysis,
            rhyme=None,
            syllable_match=None,
            score=ScoreBreakdown(rhyme=0, syllables=0),
            feedback=["Try a longer line and resubmit."],
        )

    rhyme_ok, rhyme_detail = engine.rhymes(
        prompt_last_word=prompt_analysis.last_word,
        user_last_word=user_analysis.last_word,
        mode=cfg.rhyme_mode,
    )
    rhyme = RhymeAnalysis(mode=cfg.rhyme_mode, match=rhyme_ok, details=rhyme_detail)

    difference = abs(prompt_analysis.syllables - user_analysis.syllables)
    syllable_match = SyllableMatch(
        tolerance=cfg.syllable_tolerance,
        difference=difference,
        passed=difference <= cfg.syllable_tolerance,
    )

    score = ScoreBreakdown(
        rhyme=2 if rhyme.match else 0,
        syllables=1 if syllable_match.passed else 0,
    )

    feedback = _build_feedback(rhyme, syllable_match, prompt_analysis, user_analysis)

    return EvaluationResult(
        valid=True,
        errors=[],
        prompt=prompt_analysis,
        user=user_analysis,
        rhyme=rhyme,
        syllable_match=syllable_match,
        score=score,
        feedback=feedback,
    )


def _build_feedback(
    rhyme: RhymeAnalysis,
    syllables: SyllableMatch,
    prompt: LineAnalysis,
    user: LineAnalysis,
) -> list[str]:
    messages: list[str] = []
    messages.append("Rhyme: pass." if rhyme.match else "Rhyme: not a strict match.")
    messages.append(
        f"Syllables: prompt={prompt.syllables}, user={user.syllables}, diff={syllables.difference}."
    )
    if user.unknown_words:
        messages.append(f"Unknown words: {', '.join(user.unknown_words)}")
    return messages
