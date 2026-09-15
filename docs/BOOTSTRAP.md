# Bootstrap wizard

Run from the Mac project directory with Python 3.12. No third-party Python packages are needed.

```sh
python3 scripts/bootstrap.py
python3 scripts/bootstrap.py --check
python3 scripts/bootstrap.py --apply
```

The default invocation prompts for an environment name, SSH alias, and remote absolute directory, then prints a plan without writing or connecting. `--check` offers an explicit read-only SSH check. `--apply` shows the exact remote command and profile contents, then requires typing `SETUP <profile>` before changes.

## Target state of this stage

- Mac: existing source workspace plus `environments/<profile>/bootstrap.json`.
- Remote Linux server: `<project>/checkout` and `<project>/artifacts` directories.
- Builds remain on the remote server. No Docker build runs on the Mac.
- Existing files are preserved. A different existing profile is rejected.
- SSH requires an already verified known-host entry and noninteractive authentication. Use your existing SSH configuration; do not put passwords, tokens, or key contents in the wizard.

This is workspace bootstrap, not the complete stack installer. It does not copy source, install packages, initialize Git, configure mise in a new project, run sudo, start services, or deploy Kubernetes workloads. The current project remains at its existing path; it is not renamed.

Subsequent stack setup must use Ansible for host configuration, Terraform for platform resources/namespaces, and Helm for releases. Jenkins will build images on the remote server. Those implementation files do not yet exist.

## Validation and recovery

```sh
python3 -B -m unittest discover -s scripts -p 'test_bootstrap.py' -v
```

The wizard checks CLI presence, not versions or service health. Successful SSH directory creation is not cluster readiness. On failure, earlier successful actions may remain. Inspect the printed paths before retrying. Identical profiles and directory creation are safe to repeat. To undo, remove only the generated profile and newly created directories after confirming they are empty; never remove existing source or runtime data. No automatic cleanup is performed.
