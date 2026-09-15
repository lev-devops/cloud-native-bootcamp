#!/usr/bin/env python3
"""Interactive workspace bootstrap. Preview by default; no software installs."""
import argparse
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / '.local' / 'environments'
PROBE = (
    'set -eu; test "$(uname -s)" = Linux; '
    'printf "os=Linux\\narch=%s\\n" "$(uname -m)"; '
    'for t in git docker k3s python3; do '
    'if command -v "$t" >/dev/null 2>&1; then '
    'printf "%s=available\\n" "$t"; else printf "%s=missing\\n" "$t"; fi; done'
)


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


def configuration(target, directory, control=ROOT):
    control = Path(control).expanduser().resolve()
    if not control.is_dir():
        raise ValueError('Control workspace must be an existing project directory')
    return {'schema_version': 1, 'control_workspace': str(control),
            'remote': {'ssh_host': host(target), 'workspace': remote_path(directory)},
            'image_build_location': 'remote', 'namespace_owner': 'terraform',
            'application_release_owner': 'helm'}


def remote_command(directory):
    # SSH invokes a remote shell: quote every user-supplied path.
    paths = [str(PurePosixPath(directory) / child)
             for child in ('checkout', 'artifacts')]
    # Refuse symlink ancestors before mkdir; do not adopt redirected workspaces.
    ancestors = list(reversed(PurePosixPath(directory).parents)) + [PurePosixPath(directory)]
    checks = ['test "$(uname -s)" = Linux']
    for path in [str(p) for p in ancestors] + paths:
        checks.append('test ! -L ' + shlex.quote(path))
    checks.append('mkdir -p -- ' + ' '.join(shlex.quote(p) for p in paths))
    for path in paths:
        checks.extend(['test -d ' + shlex.quote(path), 'test -w ' + shlex.quote(path)])
    return ' && '.join(checks)


def check_profile(profile, body):
    # Check the target and the directory we will create in. System paths such
    # as macOS /var -> /private/var are legitimate; do not reject them.
    if profile.is_symlink() or profile.parent.is_symlink():
        raise ValueError(f'Profile target or parent is a symlink: {profile}')
    if profile.exists() and profile.read_text(encoding='utf-8') != body:
        raise ValueError('Existing profile differs; choose another profile name')


def apply_profile(profile, config):
    """Write success configuration only after a successful remote command."""
    body = json.dumps(config, indent=2) + '\n'
    check_profile(profile, body)
    profile.parent.mkdir(parents=True, exist_ok=True)
    # Test local write access before changing the remote server.
    if not os.access(profile.parent, os.W_OK):
        raise PermissionError('Profile directory is not writable')
    subprocess.run(ssh(config['remote']['ssh_host'], remote_command(config['remote']['workspace'])),
                   check=True, timeout=30)
    check_profile(profile, body)
    if not profile.exists():
        with profile.open('x', encoding='utf-8') as output:
            output.write(body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='offer confirmation to create folders/profile')
    parser.add_argument('--check', action='store_true', help='offer read-only SSH prerequisite check')
    parser.add_argument('--name', help='environment profile name')
    parser.add_argument('--host', help='SSH alias or user@hostname (default: mint-hp)')
    parser.add_argument('--remote-dir', help='dedicated absolute remote path')
    parser.add_argument('--control-dir', type=Path, default=ROOT, help='existing local project directory')
    parser.add_argument('--non-interactive', action='store_true', help='require explicit name, host and remote-dir')
    parser.add_argument('--yes', action='store_true', help='confirm --check/--apply for scripted use')
    args = parser.parse_args()
    if platform.system() not in ('Darwin', 'Linux'):
        raise ValueError('This version supports macOS and Linux control hosts only')
    if args.non_interactive and not all((args.name, args.host, args.remote_dir)):
        parser.error('--non-interactive requires --name, --host and --remote-dir')
    if args.non_interactive and (args.apply or args.check) and not args.yes:
        parser.error('Scripted --check/--apply requires --yes')
    print('Bootstrap wizard: control workspace + remote Linux server')
    print('Stage: workspace preparation. No packages, services, containers, or cluster changes.')
    name = args.name or ask('Environment profile name', 'mint-hp')
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,62}', name):
        raise ValueError('Profile name must use lowercase letters, digits, and hyphens')
    config = configuration(args.host or ask('SSH host or alias', 'mint-hp'),
                           args.remote_dir or ask('Remote project directory (absolute, writable by SSH user)', ''),
                           args.control_dir)
    target = config['remote']['ssh_host']
    directory = config['remote']['workspace']
    profile = PROFILES / name / 'bootstrap.json'
    body = json.dumps(config, indent=2) + '\n'
    check_profile(profile, body)
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
        check = ssh(target, PROBE)
        print('\nRead-only remote discovery (does not verify service health):')
        print(shlex.join(check))
        if args.yes or input('Type CHECK to connect: ').strip() == 'CHECK':
            subprocess.run(check, check=True, timeout=30)
    if not args.apply:
        print('\nPreview complete: no profile or remote directories created. Use --apply to execute.')
        return
    print('\nNo uploads, software installs, sudo, image builds, or deployments will run.')
    if not args.yes and input(f'Type SETUP {name} to execute the displayed plan: ').strip() != f'SETUP {name}':
        print('Cancelled; no setup actions executed.')
        return
    apply_profile(profile, config)
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
