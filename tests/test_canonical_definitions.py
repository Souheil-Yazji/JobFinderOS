from pathlib import Path
import re
import subprocess
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]


class CanonicalDefinitions(unittest.TestCase):
    def test_complete_ownership_and_modes(self):
        mapping = yaml.safe_load((ROOT / "config/skill_agents.yaml").read_text())
        canonical = {p.stem for p in (ROOT / "skills").glob("*.md")}
        legacy = {p.stem for p in (ROOT / ".claude/commands").glob("*.md")}
        self.assertTrue(legacy <= canonical)
        self.assertEqual(set(mapping), canonical)
        for skill, agent in mapping.items():
            self.assertTrue((ROOT / "agents" / (agent + ".md")).is_file())
            content = (ROOT / "skills" / (skill + ".md")).read_text()
            self.assertTrue(content.startswith(f"**Agent:** `{agent}`\n"))
            self.assertRegex(content, r"\*\*Execution:\*\* (batch|interactive|orchestrated)\n")
            self.assertNotIn(".claude/", content)
            self.assertNotIn("CLAUDE.md", content)
            self.assertNotIn("subagent_type", content)
        for skill in ["jobs-daily", "mark-weekly", "jobs-priority-watch"]:
            self.assertIn(skill, mapping)

    def test_private_paths_and_tracked_exceptions(self):
        paths = [f"config/{n}.md" for n in ["profile", "scoring_rubric", "wins", "voice", "targets", "stories"]]
        paths += ["config/ats_boards.yaml", "vault/Companies/Acme/Role.md", "logs/test.log"]
        for path in paths:
            result = subprocess.run(["git", "check-ignore", "--no-index", path], cwd=ROOT, capture_output=True)
            self.assertEqual(result.returncode, 0, path)
        # Existing skeleton files remain tracked; do not claim blanket vault privacy.
        for path in ["vault/Dashboard.md", "vault/Strategy.md"]:
            result = subprocess.run(["git", "ls-files", "--error-unmatch", path], cwd=ROOT, capture_output=True)
            self.assertEqual(result.returncode, 0, path)


if __name__ == "__main__":
    unittest.main()
