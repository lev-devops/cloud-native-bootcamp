# Cloud Native Bootcamp

Public, local-first reference project for delivering a portable containerized application through Jenkins to Kubernetes. Mint HP is the first execution environment; the Mac is the source and CLI control workstation.

## Scope

- Local Mint HP/k3s implementation first.
- AWS/EKS is a later, explicitly approved phase.
- No credentials, cloud account identifiers, or secrets in Git.

## Current milestone

The working milestone is the Mac-to-remote workspace bootstrap. It previews all actions, can run a read-only SSH prerequisite check, and creates only dedicated checkout/artifact directories after explicit confirmation. The Docker image is built on the remote Linux host, not on the Mac.

```bash
python3 scripts/bootstrap.py
python3 scripts/bootstrap.py --check
python3 scripts/bootstrap.py --apply
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

The full Ansible, Terraform, Helm, Jenkins, registry, k3s, and Prometheus layers are subsequent milestones and are not represented as complete yet. See [docs/RUNBOOK.md](docs/RUNBOOK.md) for verified work and [docs/BOOTSTRAP.md](docs/BOOTSTRAP.md) for scope and recovery.

## Minimum seeder path

The supported platform-creator path uses standard Ansible commands. The local playbook creates a control workspace; the remote playbook prepares an application-host workspace. No custom orchestration script is required for this first milestone.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r ansible/requirements.txt
ansible-playbook -i ansible/inventory/localhost.ini ansible/control-local.yml --check
ansible-playbook -i ansible/inventory/localhost.ini ansible/control-local.yml
ansible-playbook -i ansible/inventory/mint-hp.ini ansible/control-remote.yml --check
```

## Tool ownership

- Terraform: infrastructure and Kubernetes platform resources.
- Ansible: Linux host preparation and configuration.
- Helm: Kubernetes application packaging and releases.
- Jenkins: build, test, scan, and promotion pipeline.
- Docker: reproducible application images.
- Prometheus: metrics and alerting.
