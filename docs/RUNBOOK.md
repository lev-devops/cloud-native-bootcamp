# Verified Runbook

Generated from append-only `docs/runbook/events.jsonl`.

Only `PASSED` events are verified. `FAILED`, `CORRECTED`, and `BLOCKED` events remain visible.

## bootstrap-wizard-tests — PASSED

- Environment: `local`
- Recorded: `2026-09-15T00:00:00Z`
- Expected: `bootstrap unit tests pass`
- Observed: `5 tests passed`
- Evidence: `scripts/test_bootstrap.py: 5 tests passed`

## public-package-docs — PASSED

- Environment: `local`
- Recorded: `2026-09-15T12:12:21.014618+00:00`
- Command: `README.md, LICENSE, CONTRIBUTING.md, SECURITY.md review`
- Expected: `Public scope and safety guidance are explicit`
- Observed: `Files present; current milestone and secret boundaries documented`
- Evidence: `working tree inspection`

## bootstrap-test-suite — PASSED

- Environment: `local`
- Recorded: `2026-09-15T12:12:21.146327+00:00`
- Command: `python3 -m unittest discover -s scripts -p 'test_*.py' -v`
- Expected: `All tests pass`
- Observed: `5 tests passed`
- Evidence: `terminal output`

## public-package-docs — PASSED

- Environment: `local`
- Recorded: `2026-09-15T12:14:34.350959+00:00`
- Command: `README.md, LICENSE, CONTRIBUTING.md, SECURITY.md review`
- Expected: `Public scope and safety guidance are explicit`
- Observed: `Files present; current milestone and secret boundaries documented`
- Evidence: `working tree inspection`

## bootstrap-test-suite — PASSED

- Environment: `local`
- Recorded: `2026-09-15T12:14:34.485612+00:00`
- Command: `python3 -m unittest discover -s scripts -p 'test_*.py' -v`
- Expected: `All tests pass`
- Observed: `5 tests passed`
- Evidence: `terminal output`

## bootstrap-regression-suite — PASSED

- Environment: `local`
- Recorded: `2026-09-15T13:00:14.260423+00:00`
- Command: `python3 -B -m unittest discover -s scripts -p 'test_*.py' -v`
- Expected: `Bootstrap behavior is safe under success, rerun, failure, and unsafe input`
- Observed: `9 tests passed`
- Evidence: `terminal output`

## mint-hp-readonly-preflight — PASSED

- Environment: `mint-hp`
- Recorded: `2026-09-15T13:00:14.309911+00:00`
- Command: `python3 scripts/bootstrap.py --non-interactive --name mint-hp --host mint-hp --remote-dir /home/lev/projects/cloud-native-bootcamp --check --yes`
- Expected: `Reachable Linux remote exposes required bootstrap CLIs`
- Observed: `Linux x86_64; git, docker, k3s, python3 available`
- Evidence: `SSH command output`

## runbook-renderer — FAILED

- Environment: `local`
- Recorded: `2026-09-15T13:01:17.481078+00:00`
- Command: `python3 scripts/runbook.py passed ...`
- Expected: `Record event and regenerate RUNBOOK.md`
- Observed: `KeyError on legacy event missing command field`
- Evidence: `terminal traceback`
- Correction: `Use e.get(label) for legacy event compatibility`

## runbook-renderer — CORRECTED

- Environment: `local`
- Recorded: `2026-09-15T13:01:17.515564+00:00`
- Command: `python3 scripts/runbook.py passed ...`
- Expected: `Legacy and new events render successfully`
- Observed: `Runbook regenerated and later events recorded`
- Evidence: `docs/RUNBOOK.md`
