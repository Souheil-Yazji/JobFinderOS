"""Helpers may change local state, but must never operate on Git."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


class LocalHelpers(unittest.TestCase):
    def test_prune_preserves_newest_and_never_runs_git(self):
        pruner = module("jobfinderos_prune_history")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "vault/Daily Digests"
            folder.mkdir(parents=True)
            old = folder / "2000-01-01.md"
            newest = folder / "2000-01-02.md"
            old.write_text("fictional old digest")
            newest.write_text("fictional latest digest")
            with patch.object(pruner, "ROOT", root), patch.object(pruner, "append_run_log"), \
                 patch("subprocess.run", side_effect=AssertionError("no subprocess allowed")), \
                 patch.object(sys, "argv", ["prune"]):
                self.assertEqual(pruner.main(), 0)
            self.assertFalse(old.exists())
            self.assertTrue(newest.exists())

    def test_ats_writes_inbox_and_seen_without_git(self):
        poller = module("jobfinderos_ats_poll")
        # An existing fixture req avoids network and real notifications.
        req = poller.Req(company="Acme", tier=1, ats="ashby", req_id="acme:1",
                         title="Widget Manager", location="Remote", url="https://example.com/jobs/1")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch.object(poller, "INBOX", root / "inbox.md"), \
                 patch.object(poller, "STATE_DIR", root), \
                 patch.object(poller, "STATE_FILE", root / "seen.json"), \
                 patch.object(poller, "LOG_FILE", root / "poll.log"), \
                 patch.object(poller, "collect", return_value=([req], [])), \
                 patch.object(poller, "apply_comp_gate", side_effect=lambda reqs: reqs), \
                 patch.object(poller, "notify"), \
                 patch("subprocess.run", side_effect=AssertionError("no Git allowed")), \
                 patch.object(sys, "argv", ["poll"]):
                self.assertEqual(poller.main(), 0)
                self.assertIn("acme:1", poller.load_seen())
            self.assertIn("Widget Manager", (root / "inbox.md").read_text())


if __name__ == "__main__":
    unittest.main()
