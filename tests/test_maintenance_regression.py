from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_local_helpers import module


class MaintenanceRegression(unittest.TestCase):
    def test_all_ats_parsers_keep_source_ids_and_urls(self):
        poller = module('jobfinderos_ats_poll')
        cases = [
            ('greenhouse', {'jobs': [{'id': '1', 'title': 'Widget Manager', 'location': {'name': 'Remote'}, 'absolute_url': 'https://example.com/1'}]}),
            ('ashby', {'jobs': [{'id': '1', 'title': 'Widget Manager', 'location': 'Remote', 'jobUrl': 'https://example.com/1', 'compensation': {'compensationTierSummary': '$120000-$140000'}}]}),
            ('lever', [{'id': '1', 'text': 'Widget Manager', 'categories': {'location': 'Remote'}, 'hostedUrl': 'https://example.com/1', 'descriptionPlain': '$120000-$140000'}]),
        ]
        for ats, payload in cases:
            with patch.object(poller, 'http_json', return_value=payload):
                rows = poller.FETCHERS[ats]({'company': 'Acme', 'slug': 'acme', 'tier': 1})
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].req_id, 'acme:1')
            self.assertEqual(rows[0].url, 'https://example.com/1')
            self.assertEqual(rows[0].location, 'Remote')
        with patch.object(poller, 'MIN_COMP', 100000):
            self.assertEqual(poller.parse_comp('$120000-$140000')[0], 'clear')
            self.assertEqual(poller.parse_comp('$60000-$80000')[0], 'under')
            self.assertEqual(poller.parse_comp('not posted')[0], 'unverified')

    def test_retention_windows_keep_newest_and_durable_notes(self):
        pruner = module('jobfinderos_prune_history')
        today = datetime(2026, 9, 14).date()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'vault/Market Intel'
            folder.mkdir(parents=True)
            names = ['Market Pulse — 2026-07-01.md', 'Market Pulse — 2026-07-02.md',
                     'Weekly Brief — 2026-07-01.md', 'Weekly Brief — 2026-08-01.md',
                     'Jobs Handoff.json', 'ATS Inbox.md']
            for name in names: (folder / name).write_text('fictional fixture')
            with patch.object(pruner, 'ROOT', root), patch.object(pruner, 'log'):
                doomed = pruner.collect(today)
            self.assertEqual([p.name for p in doomed], ['Market Pulse — 2026-07-01.md'])

    def test_latest_pointer_keeps_canonical_note_and_is_idempotent(self):
        latest = module('jobfinderos_update_latest')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            vault = root / 'vault'
            folder = vault / 'Daily Digests'
            folder.mkdir(parents=True)
            (folder / '2026-09-13.md').write_text('older synthetic digest')
            (folder / '2026-09-14.md').write_text('newest synthetic digest')
            dashboard = vault / 'Dashboard.md'
            dashboard.write_text('> Updated: 2026-09-14\nfictional dashboard')
            with patch.object(latest, 'ROOT', root), patch.object(latest, 'VAULT', vault), \
                 patch.object(latest.sys, 'argv', ['latest']):
                self.assertEqual(latest.main(), 0)
                pointer = vault / 'Daily Digest — 2026-09-14.md'
                self.assertIn('Daily Digests/2026-09-14', pointer.read_text())
                mtime = pointer.stat().st_mtime_ns
                self.assertEqual(latest.main(), 0)
                self.assertEqual(pointer.stat().st_mtime_ns, mtime)
            self.assertEqual(dashboard.read_text(), '> Updated: 2026-09-14\nfictional dashboard')


if __name__ == '__main__':
    unittest.main()
