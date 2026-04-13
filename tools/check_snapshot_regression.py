#!/usr/bin/env python3
from __future__ import annotations
import argparse
import datetime
import json
from pathlib import Path


def load_snapshot(path: Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--snapshot', default='reports/baseline_release_snapshot.json')
    ap.add_argument('--current', default='reports/snapshots')
    args = ap.parse_args()

    snap = load_snapshot(Path(args.snapshot))
    if not snap:
        print('NO-GO: baseline snapshot missing')
        return 2

    latest = sorted(Path(args.current).glob('audit_snapshot_*.md'))
    if not latest:
        print('NO-GO: no audit snapshots found')
        return 2

    latest_path = latest[-1]
    text = latest_path.read_text(encoding='utf-8')

    def get_val(label):
        for line in text.splitlines():
            if line.strip().startswith(label):
                return line.split(':', 1)[-1].strip()
        return 'n/a'

    p0 = get_val('- P0')
    rel_p0 = None
    rel_p2 = None
    in_rel = False
    for line in text.splitlines():
        if line.startswith('## Semantics completeness (relation-linked)'):
            in_rel = True
            continue
        if in_rel and line.startswith('- P0'):
            rel_p0 = line.split(':',1)[-1].strip()
        if in_rel and line.startswith('- P2'):
            rel_p2 = line.split(':',1)[-1].strip()

    print(f"Baseline snapshot: {args.snapshot}")
    print(f"Latest audit snapshot: {latest_path}")
    print(f"Current P0: {p0}")
    print(f"Relation-linked P0: {rel_p0}")
    print(f"Relation-linked P2: {rel_p2}")

    # basic gate
    if p0 != '0' or (rel_p0 and rel_p0 != '0'):
        print('NO-GO: regression detected (P0 > 0)')
        return 2
    print('OK: no regression detected in P0 buckets')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
