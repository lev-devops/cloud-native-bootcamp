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

## public-seed-verified — PASSED

- Environment: `local`
- Recorded: `2026-09-15T15:25:38.336014+00:00`
- Command: `git fetch origin; git rev-parse HEAD; git rev-parse origin/main`
- Expected: `Published seed and local main are identical`
- Observed: `Both resolve to a50888522c0aef6c0a5f239ab74965d653a44481`
- Evidence: `git command output`

## mint-hp-readonly-preflight — PASSED

- Environment: `mint-hp`
- Recorded: `2026-09-15T15:25:38.378994+00:00`
- Command: `python3 scripts/bootstrap.py --non-interactive --name mint-hp --host mint-hp --remote-dir /home/lev/projects/cloud-native-bootcamp --check --yes`
- Expected: `Remote Linux prerequisites are available`
- Observed: `Linux x86_64; git, docker, k3s, python3 available`
- Evidence: `SSH command output`

## mint-hp-workspace-bootstrap — PASSED

- Environment: `mint-hp`
- Recorded: `2026-09-15T15:26:53.001390+00:00`
- Command: `python3 scripts/bootstrap.py --non-interactive --name mint-hp --host mint-hp --remote-dir /home/lev/projects/cloud-native-bootcamp --apply --yes`
- Expected: `Dedicated checkout and artifacts directories are created and writable`
- Observed: `workspace-ready`
- Evidence: `SSH verification output`
