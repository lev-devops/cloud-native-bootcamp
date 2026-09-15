#!/usr/bin/env python3
"""Append and render verified runbook events without external dependencies."""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / 'docs' / 'runbook' / 'events.jsonl'
RUNBOOK = ROOT / 'docs' / 'RUNBOOK.md'

def now(): return datetime.now(timezone.utc).isoformat()
def record(args):
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    event = {'timestamp': now(), 'status': args.status, 'step': args.step,
             'environment': args.env, 'command': args.command or '',
             'expected': args.expect or '', 'observed': args.observed or '',
             'evidence': args.evidence or '', 'correction': args.correction or ''}
    with EVENTS.open('a', encoding='utf-8') as f: f.write(json.dumps(event, sort_keys=True) + '\n')
    render()
    print(f"recorded {args.status}: {args.step}")
def render():
    events = [json.loads(x) for x in EVENTS.read_text().splitlines() if x.strip()] if EVENTS.exists() else []
    lines = ['# Verified Runbook', '', 'Generated from append-only `docs/runbook/events.jsonl`.', '',
             'Only `PASSED` events are verified. `FAILED`, `CORRECTED`, and `BLOCKED` events remain visible.', '']
    for e in events:
        lines += [f"## {e['step']} — {e['status']}", '', f"- Environment: `{e['environment']}`", f"- Recorded: `{e['timestamp']}`"]
        for label in ('command','expected','observed','evidence','correction'):
            if e.get(label): lines.append(f"- {label.title()}: `{e[label]}`")
        lines.append('')
    RUNBOOK.write_text('\n'.join(lines), encoding='utf-8')
def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest='action', required=True)
    for status in ('STARTED','PASSED','FAILED','CORRECTED','BLOCKED'):
        q = sub.add_parser(status.lower()); q.set_defaults(status=status)
        q.add_argument('--step', required=True); q.add_argument('--env', default='local')
        q.add_argument('--command'); q.add_argument('--expect'); q.add_argument('--observed')
        q.add_argument('--evidence'); q.add_argument('--correction')
    args = p.parse_args(); record(args)
if __name__ == '__main__': main()
