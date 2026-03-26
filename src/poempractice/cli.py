from __future__ import annotations

import json

from poempractice.evaluator import evaluate_submission


def main() -> None:
    print("Enter prompt line:")
    prompt = input().strip()
    print("Enter user line:")
    user = input().strip()

    result = evaluate_submission(prompt, user)
    print(json.dumps(_to_json(result), indent=2))


def _to_json(result):
    return {
        "valid": result.valid,
        "errors": result.errors,
        "prompt": None
        if result.prompt is None
        else {
            "last_word": result.prompt.last_word,
            "syllables": result.prompt.syllables,
            "normalized_words": result.prompt.normalized_words,
        },
        "user": None
        if result.user is None
        else {
            "last_word": result.user.last_word,
            "syllables": result.user.syllables,
            "normalized_words": result.user.normalized_words,
        },
        "rhyme": None
        if result.rhyme is None
        else {
            "mode": result.rhyme.mode,
            "match": result.rhyme.match,
            "details": result.rhyme.details,
        },
        "syllable_match": None
        if result.syllable_match is None
        else {
            "tolerance": result.syllable_match.tolerance,
            "difference": result.syllable_match.difference,
            "pass": result.syllable_match.passed,
        },
        "score": result.score.total,
        "score_breakdown": {
            "rhyme": result.score.rhyme,
            "syllables": result.score.syllables,
            "bonus_exact_syllables": result.score.bonus_exact_syllables,
        },
        "feedback": result.feedback,
    }


if __name__ == "__main__":
    main()
