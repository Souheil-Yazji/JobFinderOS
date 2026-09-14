from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from test_local_helpers import module


class WatchClock(datetime):
    @classmethod
    def now(cls, tz=None):
        return cls(2026, 9, 14, 12, tzinfo=timezone.utc)


class PriorityWatch(unittest.TestCase):
    def test_success_marker_and_skip_prevent_duplicate_runs(self):
        watch = module('jobfinderos_priority_watch')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(watch, 'datetime', WatchClock), \
                 patch.object(watch, 'MARKER', root / 'success'), \
                 patch.object(watch, 'LOCK', root / 'lock'), \
                 patch.object(watch, '_scheduler_cfg', return_value={'watch': {'hour': 9}}), \
                 patch.object(watch, 'emit') as emit, \
                 patch.object(watch.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run:
                watch.main()
                self.assertEqual((root / 'success').read_text().strip(), '2026-09-14')
                self.assertFalse((root / 'lock').exists())
                self.assertEqual(run.call_args.args[0][-1], 'jobs-priority-watch')
                watch.main()
                self.assertEqual(run.call_count, 1)
                self.assertEqual(emit.call_args.args[0]['reason'], 'already_succeeded')

    def test_failure_does_not_mark_success(self):
        watch = module('jobfinderos_priority_watch')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(watch, 'datetime', WatchClock), \
                 patch.object(watch, 'MARKER', root / 'success'), \
                 patch.object(watch, 'LOCK', root / 'lock'), \
                 patch.object(watch, '_scheduler_cfg', return_value={'watch': {'hour': 9}}), \
                 patch.object(watch, 'emit') as emit, \
                 patch.object(watch.subprocess, 'run', return_value=subprocess.CompletedProcess([], 17, '', 'failed')):
                watch.main()
                self.assertFalse((root / 'success').exists())
                self.assertFalse((root / 'lock').exists())
                self.assertEqual(emit.call_args.args[0]['status'], 'error')


if __name__ == '__main__':
    unittest.main()
