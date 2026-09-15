# Deterministic Runbook

This is the stable operating guide. It is not an execution log. Every command below has a defined target state and must be recorded separately in [`docs/runbook/EXECUTION_LOG.jsonl`](runbook/EXECUTION_LOG.jsonl) with `scripts/runbook.py`.

## Control environment

Run from the Mac project checkout:

```sh
python3 /Users/lev/.codex/skills/configure-codex-mise/scripts/manage_mise.py verify --project "$PWD"
python3 -B -m unittest discover -s scripts -p 'test_*.py' -v
```

Target state: the declared toolchain resolves and all local tests pass.

## Remote preflight

```sh
python3 scripts/bootstrap.py --non-interactive --name mint-hp --host mint-hp --remote-dir /home/lev/projects/cloud-native-bootcamp --check --yes
```

Target state: Mint HP responds over verified SSH and reports Linux with required bootstrap tools.

## Minimum control-environment seeder

From the seed checkout, use a Python virtual environment and Ansible itself:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r ansible/requirements.txt
ansible-playbook -i ansible/inventory/localhost.ini ansible/control-local.yml --syntax-check
ansible-playbook -i ansible/inventory/localhost.ini ansible/control-local.yml --check -e control_root="$HOME/platform-control"
ansible-playbook -i ansible/inventory/localhost.ini ansible/control-local.yml -e control_root="$HOME/platform-control"
```

Target state: a supported Mac/Linux control host has a new or empty explicit target with `~/platform-control/{environments,generated,logs}` and a `CONTROL_ENVIRONMENT` identity file. The check mode must pass before the apply command. A non-empty target is refused. After reviewing it, explicitly opt in with `-e control_overwrite=true`; this does not delete unrelated files. The seed checkout is not modified. Command availability checks execute read-only during check mode.

Record each command in `docs/runbook/EXECUTION_LOG.jsonl`.

## Remote workspace bootstrap

Review the printed command, then run:

```sh
python3 scripts/bootstrap.py --non-interactive --name mint-hp --host mint-hp --remote-dir /home/lev/projects/cloud-native-bootcamp --apply --yes
```

Verify:

```sh
ssh mint-hp 'test -w /home/lev/projects/cloud-native-bootcamp/checkout && test -w /home/lev/projects/cloud-native-bootcamp/artifacts && echo workspace-ready'
```

Target state: dedicated writable remote directories exist. No packages, images, Kubernetes objects, or services are changed by this stage.

## Evidence rules

- Record command, environment, expected result, observed result, and evidence path.
- `PASSED` means the observed result meets the expected result.
- `FAILED` remains in the log; do not delete it.
- A `CORRECTED` entry must identify the fix, and all dependent steps must be run again.
- The log is append-only; this guide changes only when the deterministic procedure changes.

## Historical verification

- Bootstrap wizard tests originally passed: 5 tests.
- Hardened regression suite passes: 10 tests.
- Mint HP read-only preflight passed: Linux x86_64; Git, Docker, k3s, and Python available.
- Mint HP workspace bootstrap passed: checkout and artifacts directories writable.
