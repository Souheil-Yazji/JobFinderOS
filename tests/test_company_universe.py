"""Fictional state only: ownership, lifecycle records and bounded discovery."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import jobfinderos_agent_runner as runner
from jobfinderos_company_universe import (
    QUEUE, UNIVERSE, scaffold, validate_queue, validate_universe,
)


def lead(company="Acme Widgets", status="unreviewed", author="Scout", score="8.2"):
    return (f"| {company} | https://example.com/jobs/1 | Relevant widget role | 2026-09-14 | "
            f"{status} | Widget Lead | {score} | https://example.com/careers | {author} | — |\n")


def company(name="Acme Widgets", status="Tier 2", score="8.2", url="https://example.com/careers"):
    return (f"| {name} | {status} | {score} | Widget systems | {url} | Company site | "
            f"Widget ownership | 2026-09-14 | [[Companies/{name}/Company Evaluation]] |\n")


class CompanyTables(unittest.TestCase):
    def test_first_run_and_template_compatibility(self):
        self.assertEqual(validate_queue(scaffold(QUEUE)), [])
        self.assertEqual(validate_universe(scaffold(UNIVERSE)), [])
        templates = (ROOT / "docs/vault-note-templates.md").read_text()
        for name in (QUEUE, UNIVERSE):
            self.assertIn(scaffold(name), templates)
    def test_queue_duplicate_status_and_score_validation(self):
        for body in (lead() + lead("acme  widgets"), lead(status="Tier 1"), lead(score="nan")):
            with self.subTest(body=body), self.assertRaises(ValueError):
                validate_queue(scaffold(QUEUE) + body)

    def test_invalid_tier_score_date_and_url(self):
        for row in (company(status="Tier 3"), company(status="Tier 1", score="8.49"),
                    company(score="NaN"), company(score="11"), company(url="javascript:alert(1)"),
                    company().replace("2026-09-14", "2026-02-30")):
            with self.subTest(row=row), self.assertRaises(ValueError):
                validate_universe(scaffold(UNIVERSE) + row)
        self.assertEqual(len(validate_universe(scaffold(UNIVERSE) + company(status="Watch", url="Unknown"))), 1)

    def test_caps_and_rejected_history(self):
        for status, maximum, fit in (("Tier 1", 10, "9"), ("Tier 2", 25, "8")):
            text = scaffold(UNIVERSE) + "".join(company(f"Widgets {i}", status, fit) for i in range(maximum))
            self.assertEqual(len(validate_universe(text)), maximum)
            with self.assertRaises(ValueError):
                validate_universe(text + company("Overflow Widgets", status, fit))
        rows = validate_universe(scaffold(UNIVERSE) + company(status="Rejected", score="4", url="Unknown"))
        self.assertEqual(rows[0]["Status"], "Rejected")


class UniverseBoundaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root_patch = patch.object(runner, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_mark_can_maintain_only_the_two_new_tracking_notes(self):
        before = runner.snapshot()
        self.write(QUEUE, scaffold(QUEUE) + lead(author="Mark"))
        self.write(UNIVERSE, scaffold(UNIVERSE) + company())
        after = runner.snapshot()
        self.assertEqual(runner.violations("mark", "company-discovery", before, after), [])
        self.write("vault/Tracking/Contacts.md", "Unauthorized contact change")
        self.assertEqual(runner.violations("mark", "company-discovery", after, runner.snapshot()),
                         ["vault/Tracking/Contacts.md"])

    def test_scout_cannot_write_company_state_in_phase_two(self):
        self.write(QUEUE, scaffold(QUEUE))
        self.write(UNIVERSE, scaffold(UNIVERSE) + company())
        before = runner.snapshot()
        self.write(QUEUE, scaffold(QUEUE) + lead("New Widgets"))
        self.assertEqual(runner.violations("scout", "jobs-scout", before, runner.snapshot()), [QUEUE])
        self.write(UNIVERSE, scaffold(UNIVERSE) + company(status="Tier 1", score="9"))
        self.assertEqual(runner.violations("scout", "jobs-scout", before, runner.snapshot()), [QUEUE, UNIVERSE])

    def test_mark_cannot_create_job_opportunity_notes(self):
        before = runner.snapshot()
        role = "vault/Companies/Acme Widgets/Acme Widgets — Widget Lead.md"
        self.write(role, "- **Stage:** Spotted\n")
        self.assertEqual(runner.violations("mark", "company-discovery", before, runner.snapshot()), [role])

    def test_coach_cannot_promote_and_mark_cannot_delete_registry(self):
        before = runner.snapshot()
        self.write(UNIVERSE, scaffold(UNIVERSE) + company())
        self.assertEqual(runner.violations("coach", "checkin", before, runner.snapshot()), [UNIVERSE])
        before = runner.snapshot()
        (self.root / UNIVERSE).unlink()
        self.assertEqual(runner.violations("mark", "company-discovery", before, runner.snapshot()), [UNIVERSE])

    def test_non_mark_cannot_write_evaluations_and_bad_tiers_fail_audit(self):
        before = runner.snapshot()
        evaluation = "vault/Companies/Acme Widgets/Company Evaluation.md"
        self.write(evaluation, "Unsupported company score")
        self.assertEqual(runner.violations("scout", "jobs-scout", before, runner.snapshot()), [evaluation])
        self.write(UNIVERSE, scaffold(UNIVERSE) + company(status="Tier 1", score="5"))
        self.assertEqual(runner.violations("mark", "company-discovery", before, runner.snapshot()), [UNIVERSE])


if __name__ == "__main__":
    unittest.main()
