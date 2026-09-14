import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('scheduler', ROOT / 'scripts/scheduler_tick.py')
scheduler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scheduler)


class Clock(datetime):
    def astimezone(self, tz=None):
        return self

    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 14, 12, tzinfo=timezone.utc)


class Scheduler(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / 'state.json'
        for target, replacement in [('project_root', lambda: ROOT), ('state_path', lambda: self.state),
                                    ('lock_path', lambda: self.root / 'lock'), ('datetime', Clock)]:
            p = patch.object(scheduler, target, replacement)
            p.start(); self.addCleanup(p.stop)
        self.log = patch.object(scheduler, 'append_run_log').start()
        self.addCleanup(patch.stopall)

    def main(self, *args):
        with patch.object(sys, 'argv', ['scheduler', *args]):
            return scheduler.main()

    def test_weekly_wins_and_state_written_only_on_success(self):
        with patch.object(scheduler, 'run_skill', return_value=17) as run, patch.object(scheduler, 'run_watch_guards'):
            self.assertEqual(self.main(), 17)
            self.assertFalse(self.state.exists())
            self.assertEqual(run.call_args.args[1:], ('mark-weekly', 'mark-weekly'))
        with patch.object(scheduler, 'run_skill', return_value=0), patch.object(scheduler, 'run_watch_guards'):
            self.assertEqual(self.main(), 0)
        state = json.loads(self.state.read_text())
        self.assertEqual(state['last_daily_date'], '2026-09-14')
        with patch.object(scheduler, 'run_skill') as run, patch.object(scheduler, 'run_watch_guards') as watch:
            self.assertEqual(self.main(), 0)
            run.assert_not_called()
            watch.assert_called_once()

    def test_dry_run_has_no_side_effects(self):
        with patch.object(scheduler, 'lock_path', side_effect=AssertionError('no lock')), \
             patch.object(scheduler, 'run_skill', side_effect=AssertionError('no model')):
            self.assertEqual(self.main('--dry-run'), 0)
        self.log.assert_not_called()
        self.assertEqual(list(self.root.iterdir()), [])

    def test_catchup_iso_year_and_daily_windows(self):
        cfg = {'weekly': {'weekday': 1, 'hour': 8}, 'daily': {'hour': 7}}
        now = datetime(2027, 1, 1, 12, tzinfo=timezone.utc)
        self.assertEqual(scheduler.iso_week_tuple(now.date()), (2026, 53))
        self.assertTrue(scheduler.weekly_is_due({}, now, cfg))
        state = {'last_weekly_iso_year': 2026, 'last_weekly_iso_week': 53}
        self.assertFalse(scheduler.weekly_is_due(state, now, cfg))
        self.assertTrue(scheduler.daily_is_due(state, now, cfg, False))
        self.assertFalse(scheduler.daily_is_due(state, now, cfg, True))
        self.assertFalse(scheduler.daily_is_due({}, now.replace(hour=6), cfg, False))

    def test_routes_scheduler_to_explicit_agent(self):
        with patch.object(scheduler.subprocess, 'run') as run:
            run.return_value.returncode = 0
            self.assertEqual(scheduler.run_skill(ROOT, 'priority-watch', 'jobs-priority-watch'), 0)
        self.assertEqual(run.call_args.args[0][2:], ['scout', 'jobs-priority-watch', '--label', 'priority-watch'])
        self.assertTrue(run.call_args.args[0][1].endswith('JobFinderOS_run_agent.sh'))


if __name__ == '__main__':
    unittest.main()
