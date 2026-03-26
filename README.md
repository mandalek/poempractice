# poempractice

A starter implementation for evaluating a user-provided second line in a couplet game.

## What is implemented

- Input normalization (case + punctuation insensitive)
- Minimum word validation
- Strict rhyme check (baseline heuristic)
- Syllable count comparison with ± tolerance
- Simple scoring (rhyme=2, syllables=1)
- Clear interfaces so you can replace rhyme/syllable algorithms later

## Quick start

```bash
python -m pip install -e .
python -m poempractice.cli
```

## Tests

```bash
python -m pytest -q
```
