from poempractice.evaluator import evaluate_submission
from poempractice.models import EvaluationConfig


def test_happy_path_score_is_three():
    result = evaluate_submission(
        "A husky howls at the full moon",
        "A lonely wolf begins to croon",
    )
    assert result.valid is True
    assert result.rhyme is not None and result.rhyme.match is True
    assert result.syllable_match is not None and result.syllable_match.passed is True
    assert result.score.total == 3


def test_line_too_short_is_invalid():
    result = evaluate_submission(
        "A husky howls at the full moon",
        "Moon soon",
    )
    assert result.valid is False
    assert any("LINE_TOO_SHORT" in err for err in result.errors)
    assert result.score.total == 0


def test_case_and_punctuation_are_ignored():
    result = evaluate_submission(
        "A husky howls at the full moon!",
        "A lone coyote starts to CROON...",
    )
    assert result.valid is True
    assert result.rhyme is not None and result.rhyme.match is True


def test_syllable_tolerance_can_be_configured():
    cfg = EvaluationConfig(syllable_tolerance=0)
    result = evaluate_submission(
        "Wind over water",
        "Sound over daughter",
        config=cfg,
    )
    assert result.valid is True
    assert result.syllable_match is not None
    assert result.syllable_match.tolerance == 0
