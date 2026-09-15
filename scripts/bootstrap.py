#!/usr/bin/env python3
"""Interactive workspace bootstrap. Preview by default; no software installs."""
import argparse
import json
import re
import shlex
import shutil
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def remote_path(value):
    path = PurePosixPath(value)
    if not path.is_absolute() or '..' in path.parts or len(path.parts) < 4:
        raise ValueError('Use a dedicated absolute remote path, e.g. /home/lev/projects/cloud-native-bootcamp')
    if any(ord(c) < 32 for c in value):
        raise ValueError('Control characters are not allowed in paths')
    return str(path)


def host(value):
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.@-]*', value):
        raise ValueError('Use an SSH config alias, hostname, or user@hostname')
    return value


def ask(label, default):
    return input(f'{label} [{default}]: ').strip() or default


def ssh(target, command):
    return ['ssh', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
            '-o', 'ConnectTimeout=10', target, command]


def configuration(target, directory):
    return {'schema_version': 1, 'control_workspace': str(ROOT),
            'remote': {'ssh_host': host(target), 'workspace': remote_path(directory)},
            'image_build_location': 'remote', 'namespace_owner': 'terraform',
            'application_release_owner': 'helm'}


def remote_command(directory):
    # SSH invokes a remote shell: quote every user-supplied path.
    paths = [str(PurePosixPath(directory) / child)
             for child in ('checkout', 'artifacts')]
    return 'mkdir -p -- ' + ' '.join(shlex.quote(p) for p in paths)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='offer confirmation to create folders/profile')
    parser.add_argument('--check', action='store_true', help='offer read-only SSH prerequisite check')
    args = parser.parse_args()
    print('Bootstrap wizard: Mac control workspace + remote Linux server')
    print('Stage: workspace preparation. No packages, services, containers, or cluster changes.')
    name = ask('Environment profile name', 'mint-hp')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,62}', name):
        raise ValueError('Profile name must use lowercase letters, digits, and hyphens')
    config = configuration(ask('SSH host or alias', 'mint-hp'),
                           ask('Remote project directory', '/home/lev/projects/cloud-native-bootcamp'))
    target = config['remote']['ssh_host']
    directory = config['remote']['workspace']
    profile = ROOT / 'environments' / name / 'bootstrap.json'
    body = json.dumps(config, indent=2) + '\n'
    if profile.is_symlink() or (profile.exists() and profile.read_text() != body):
        raise ValueError(f'Existing profile differs; choose another profile name: {profile}')
    command = ssh(target, remote_command(directory))
    print('\n1. Local tool discovery (presence only):')
    for tool in ('git', 'mise', 'ssh', 'terraform', 'ansible-playbook', 'helm', 'kubectl'):
        print(f'  {tool}: {shutil.which(tool) or "MISSING"}')
    print('\n2. Local profile to create, preserving identical existing content:')
    print(profile)
    print(body)
    print('3. Remote command (creates only checkout/artifacts directories):')
    print(shlex.join(command))
    if args.check:
        check = ssh(target, 'uname -s; uname -m; for t in git docker k3s; do command -v "$t" || true; done')
        print('\nRead-only remote discovery (does not verify service health):')
        print(shlex.join(check))
        if input('Type CHECK to connect: ').strip() == 'CHECK':
            subprocess.run(check, check=True, timeout=30)
    if not args.apply:
        print('\nPreview complete: no profile or remote directories created. Use --apply to execute.')
        return
    print('\nNo uploads, software installs, sudo, image builds, or deployments will run.')
    if input(f'Type SETUP {name} to execute the displayed plan: ').strip() != f'SETUP {name}':
        print('Cancelled; no setup actions executed.')
        return
    subprocess.run(command, check=True, timeout=30)
    profile.parent.mkdir(parents=True, exist_ok=True)
    if not profile.exists():
        with profile.open('x') as output:
            output.write(body)
    print(f'Workspace preparation complete: {profile}')
    print('Stack installation and service readiness remain unverified.')
    print('Reruns preserve identical profiles and existing directories.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        raise SystemExit(f'Bootstrap failed: {error}. Earlier completed actions may remain; inspect before retrying.')
    except (EOFError, KeyboardInterrupt):
        raise SystemExit('Cancelled.')
