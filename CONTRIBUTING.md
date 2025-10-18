# Contributing

Thanks for your interest in contributing! A few quick guidelines:

- Keep scope small and focused. This project aims to stay tiny and dependency-free.
- For new features, open an issue first to discuss the use case.
- Include tests for behavior changes in `tests/` (simple functions are fine).
- Run a quick smoke test locally before opening a PR.

## Dev quickstart

```bash
python3 file_organizer.py --dry-run
python3 file_organizer.py ~/Downloads --recursive --dry-run
```

## Project goals (design principles)
- Stdlib-only, minimal code, clear behavior.
- Safety by default (no recursion, no moving no-extension files unless asked).
- Predictable, testable, documented.

## Release process
- Update `CHANGELOG.md`.
- Tag a version (e.g., `v0.1.0`).
- Create a GitHub Release with highlights.
