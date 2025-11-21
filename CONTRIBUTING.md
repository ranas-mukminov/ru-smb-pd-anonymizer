# Contributing

Thanks for helping improve `ru-smb-pd-anonymizer`.

## How to contribute
- Open an issue with context (use-case, data volume, compliance constraints).
- For PRs: keep changes small and focused; add tests; update docs/CHANGELOG where relevant.
- Do not include real personal data in issues, commits, fixtures, or logs. Use synthetic examples only.
- Follow the legal disclaimers: the project is technical; legal assessment belongs to counsel/compliance.

## Development setup
- Python 3.10+.
- Install dev deps: `pip install -e .[dev,test]`.
- Run checks: `scripts/lint.sh` then `pytest`.
- Security: `scripts/security_scan.sh`.
- Performance smoke: `scripts/perf_check.sh`.

## Code style
- Type hints everywhere; keep functions small.
- Avoid logging raw PII in tests, samples, or debug output.
- Prefer deterministic, reversible transforms only where policies allow.
