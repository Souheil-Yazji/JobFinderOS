#!/usr/bin/env python3
"""Optional real-CLI smoke harness. Uses committed files and fictional state only."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def validate(root, expect_prep=True):
    vault = root / 'vault'
    opportunities = [p for p in (vault / 'Companies').rglob('*.md')
                     if re.search(r'^-?\s*\*\*Stage:\*\*', p.read_text(), re.M)]
    assert len(opportunities) == 1, 'Expected only the eligible fictional role'
    role = opportunities[0].read_text()
    assert 'Widget Engineering Manager' in role and '8/10' in role
    assert 'Spotted' in role, 'An agent changed the application stage'
    assert not list((vault / 'Outreach Drafts').glob('*.md')), 'Unexpected outreach'
    assert list((vault / 'Market Intel').glob('Market Pulse*.md'))
    assert (vault / 'Market Intel/Jobs Handoff.json').is_file()
    digests = list((vault / 'Daily Digests').glob('*.md'))
    assert digests and 'synthetic' in digests[-1].read_text().lower()
    if expect_prep:
        assert list((vault / 'Companies').rglob('*Interview Prep*Screen*.md'))
    records = [json.loads(p.read_text()) for p in (root / 'logs/agent-runs').glob('*/run.json')]
    assert records and all(r['exit_code'] == 0 and not r['boundary_violations'] for r in records)
    print(json.dumps({'status': 'passed', 'runs': len(records), 'opportunities': len(opportunities)}, indent=2))


def prepare():
    root = Path(tempfile.mkdtemp(prefix='jobfinderos-fictional-')).resolve()
    archive = root / 'source.tar'
    subprocess.run(['git', 'archive', '--format=tar', '-o', str(archive), 'HEAD'], cwd=ROOT, check=True)
    with tarfile.open(archive) as source:
        # Git archive is from this repository's committed tree, not external input.
        source.extractall(root)
    archive.unlink()
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    fixture = root / 'tests/fixtures/fictional'
    for name in ['profile.md', 'scoring_rubric.md', 'stories.md']:
        shutil.copy(fixture / name, root / 'config' / name)
    (root / 'vault/Stories').mkdir(exist_ok=True)
    shutil.copy(fixture / 'Widget-Prototype.md', root / 'vault/Stories/Widget Prototype.md')
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', choices=['codex', 'claude'], default='codex')
    parser.add_argument('--execute', action='store_true', help='Run real CLI sessions with saved authentication')
    parser.add_argument('--validate', type=Path, help='Validate an existing fixture run without executing models')
    args = parser.parse_args()
    if args.validate:
        validate(args.validate)
        return 0
    root = prepare()
    print(f'Fictional repository: {root}', flush=True)
    if not args.execute:
        print('Prepared only. --execute runs real CLI sessions and uses the selected account.')
        return 0
    env = dict(os.environ, JOBFINDEROS_RUNTIME=args.runtime, JOBFINDEROS_PYTHON=sys.executable)
    fixture_instructions = ('Offline fictional smoke test. Use tests/fixtures/fictional/ats.md, market.md and email.md '
                            'as supplied primary-source snapshots and the fictional story library. '
                            'No external browsing or connectors. Label outputs synthetic, preserve role stages, '
                            'apply exclusions, and do not draft outreach. Do not invent missing details; flag fixture gaps.')
    for agent, skill, extra in [('scout', 'jobs-scout', []), ('mark', 'mark-pulse', []),
                               ('coach', 'jobs-digest', []),
                               ('coach', 'jobs-prep', ['Acme Widgets', 'Widget Engineering Manager', 'Screen'])]:
        subprocess.run(['/bin/bash', str(root / 'scripts/JobFinderOS_run_agent.sh'), agent, skill,
                        '--', *extra, fixture_instructions], cwd=root, env=env, check=True)
    validate(root)
    subprocess.run(['/bin/bash', str(root / 'scripts/verify_local_automation.sh')], cwd=root, check=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
