import json
import fcntl
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class AgentRunner(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repository with spaces'
        self.root.mkdir()
        for directory in ['scripts', 'agents', 'skills', 'docs']:
            shutil.copytree(ROOT / directory, self.root / directory, ignore=shutil.ignore_patterns('__pycache__'))
        (self.root / 'config').mkdir()
        for name in ['skill_agents.yaml', 'agent_result.schema.json', 'recruiter_playbook.md']:
            shutil.copy(ROOT / 'config' / name, self.root / 'config' / name)
        for name in ['profile', 'scoring_rubric']:
            (self.root / 'config' / (name + '.md')).write_text('Fictional candidate: Alex Example. Widget engineering. Exclude BadCo. Minimum score 7.')
        (self.root / 'vault/Automation').mkdir(parents=True)
        self.fake = Path(self.temp.name) / 'fake codex'
        self.fake.write_text('#!' + sys.executable + '\n' + '''import json, os, pathlib, re, sys, time
prompt = sys.stdin.read()
root = pathlib.Path.cwd()
(root / 'logs/call.json').write_text(json.dumps({'cwd': str(root), 'args': sys.argv[1:], 'prompt': prompt}))
skill = re.search(r'Read and execute skills/([a-z-]+)[.]md', prompt).group(1)
with (root / 'logs/calls.jsonl').open('a') as f: f.write(json.dumps({'skill': skill}) + '\\n')
if os.environ.get('FAKE_FAIL_SKILL') == skill: sys.exit(17)
if skill == 'jobs-research':
    arguments = json.loads(re.search(r'Task arguments .*?: (.*)', prompt).group(1))
    company = arguments[0]
    p = root / 'vault/Companies' / company / (company + '.md')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('Fictional company profile')
scenario = os.environ.get('FAKE_SCENARIO', '')
if scenario == 'timeout': time.sleep(10)
if scenario == 'fail': sys.exit(17)
if scenario == 'outreach':
    p = root / 'vault/Outreach Drafts/forbidden.md'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('unauthorized draft')
if scenario == 'stage':
    (root / 'vault/role.md').write_text('- **Stage:** Offer')
if scenario != 'no-result':
    result = pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1])
    result.write_text(json.dumps({'status': 'blocked' if scenario == 'blocked' else 'complete', 'summary': 'Fictional result'}))
''')
        self.fake.chmod(0o755)
        self.env = dict(os.environ, CODEX_BIN=str(self.fake), JOBFINDEROS_PYTHON=sys.executable,
                        JOBFINDEROS_RUNTIME='codex')
        self.env.pop('JOBFINDEROS_SKILL_TIMEOUT_SEC', None)

    def run_agent(self, *args):
        return subprocess.run(['/bin/bash', str(self.root / 'scripts/JobFinderOS_run_agent.sh'), *args],
                              cwd=self.temp.name, env=self.env, text=True, capture_output=True)

    def records(self):
        return [json.loads(p.read_text()) for p in (self.root / 'logs/agent-runs').glob('*/run.json')]

    def test_invalid_names_and_mismatch(self):
        for pair in [('unknown', 'jobs-scout'), ('scout', 'missing'), ('coach', 'jobs-scout'), ('scout', '../jobs-scout')]:
            self.assertNotEqual(self.run_agent(*pair).returncode, 0, pair)
        self.assertFalse((self.root / 'logs').exists())

    def test_dry_run_without_cli_profile_or_writes(self):
        self.fake.unlink()
        (self.root / 'config/profile.md').unlink()
        result = self.run_agent('scout', 'jobs-scout', '--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Agent file: agents/scout.md', result.stdout)
        self.assertFalse((self.root / 'logs').exists())

    def test_root_arguments_completion_and_logs(self):
        result = self.run_agent('coach', 'jobs-prep', '--', 'Acme Labs', 'Widget Lead', 'HM round; $(false)')
        self.assertEqual(result.returncode, 0, result.stderr)
        call = json.loads((self.root / 'logs/call.json').read_text())
        self.assertEqual(call['cwd'], str(self.root.resolve()))
        self.assertIn('HM round; $(false)', call['prompt'])
        self.assertIn('--sandbox', call['args'])
        self.assertEqual(self.records()[0]['exit_code'], 0)
        self.assertEqual(self.records()[0]['runtime'], 'codex')
        self.assertTrue((self.root / 'logs/launchd-runs.log').exists())

    def test_failure_blocked_and_missing_result(self):
        for scenario, code in [('fail', 17), ('blocked', 3), ('no-result', 3)]:
            self.env['FAKE_SCENARIO'] = scenario
            result = self.run_agent('scout', 'jobs-scout')
            self.assertEqual(result.returncode, code, result.stderr)

    def test_timeout_is_logged(self):
        self.env.update(FAKE_SCENARIO='timeout', JOBFINDEROS_SKILL_TIMEOUT_SEC='1')
        self.assertEqual(self.run_agent('scout', 'jobs-scout').returncode, 124)
        self.assertEqual(self.records()[0]['exit_code'], 124)

    def test_boundaries_include_ignored_style_outputs(self):
        self.env['FAKE_SCENARIO'] = 'outreach'
        self.assertEqual(self.run_agent('scout', 'jobs-scout').returncode, 4)
        self.assertIn('vault/Outreach Drafts/forbidden.md', self.records()[0]['boundary_violations'])
        self.env['FAKE_SCENARIO'] = 'stage'
        (self.root / 'vault/role.md').write_text('- **Stage:** Applied')
        self.assertEqual(self.run_agent('mark', 'mark-pulse').returncode, 4)

    def test_interactive_skill_rejects_batch(self):
        self.assertNotEqual(self.run_agent('coach', 'mock-interview').returncode, 0)

    def test_missing_cli_propagates_and_logs(self):
        self.fake.unlink()
        self.assertEqual(self.run_agent('scout', 'jobs-scout').returncode, 127)
        self.assertEqual(self.records()[0]['exit_code'], 127)

    def test_overlapping_manual_runs_are_rejected(self):
        (self.root / 'logs').mkdir()
        with (self.root / 'logs/agent.lock').open('a+') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertEqual(self.run_agent('scout', 'jobs-scout').returncode, 75)
        self.assertFalse((self.root / 'logs/call.json').exists())

    def test_single_agent_smoke_interfaces(self):
        for agent, skill in [('scout', 'jobs-scout'), ('mark', 'mark-pulse'), ('coach', 'jobs-digest'), ('coach', 'jobs-prep')]:
            result = self.run_agent(agent, skill)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_daily_real_process_sequence_and_one_final_record(self):
        result = self.run_agent('coach', 'jobs-daily')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('Fictional result'), 1)
        calls = [json.loads(line)['skill'] for line in (self.root / 'logs/calls.jsonl').read_text().splitlines()]
        self.assertEqual(calls, ['mark-pulse', 'jobs-scout', 'jobs-email', 'jobs-digest', 'jobs-daily-finalize'])
        manifests = list((self.root / 'logs/daily-runs').glob('*/run.json'))
        self.assertEqual(len(manifests), 1)
        manifest = json.loads(manifests[0].read_text())
        self.assertEqual(manifest['status'], 'complete')
        self.assertEqual(len(manifest['children']), 5)
        log = (self.root / 'logs/launchd-runs.log').read_text()
        self.assertEqual(log.count('— jobs-daily — completed'), 1)

    def test_daily_stops_at_every_failed_child(self):
        sequence = ['mark-pulse', 'jobs-scout', 'jobs-email', 'jobs-digest', 'jobs-daily-finalize']
        for index, skill in enumerate(sequence):
            self.env['FAKE_FAIL_SKILL'] = skill
            (self.root / 'logs').mkdir(exist_ok=True)
            (self.root / 'logs/calls.jsonl').write_text('')
            result = self.run_agent('coach', 'jobs-daily')
            self.assertEqual(result.returncode, 17, result.stderr)
            calls = [json.loads(line)['skill'] for line in (self.root / 'logs/calls.jsonl').read_text().splitlines()]
            self.assertEqual(calls, sequence[:index + 1])

    def test_prep_runs_mark_prerequisite(self):
        result = self.run_agent('coach', 'jobs-prep', '--', 'NewCo', 'Widget Lead', 'Screen')
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [json.loads(line)['skill'] for line in (self.root / 'logs/calls.jsonl').read_text().splitlines()]
        self.assertEqual(calls, ['jobs-research', 'jobs-prep'])

    def test_claude_adapter_selection(self):
        self.fake.write_text('#!' + sys.executable + '\nimport json\nprint(json.dumps({"status":"complete", "summary":"Fictional Claude result"}))\n')
        self.env.update(JOBFINDEROS_RUNTIME='claude', CLAUDE_BIN=str(self.fake))
        result = self.run_agent('scout', 'jobs-scout')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.records()[0]['runtime'], 'claude')


if __name__ == '__main__':
    unittest.main()
