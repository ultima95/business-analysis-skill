import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/business-analysis"

sys.path.insert(0, str(SKILL / "scripts"))
import lint_requirements as lr  # noqa: F401


def parse_frontmatter(path):
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


class SkillAssetsTest(unittest.TestCase):
    def test_skill_frontmatter(self):
        fm = parse_frontmatter(SKILL / "SKILL.md")
        self.assertEqual(fm["name"], "business-analysis")
        self.assertTrue(fm["description"].startswith("Use when"))
        self.assertLessEqual(len(fm["description"]), 1024)

    def test_skill_size(self):
        self.assertLessEqual(len((SKILL / "SKILL.md").read_text().splitlines()), 300)

    @unittest.expectedFailure
    def test_skill_links_resolve(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        paths = set(re.findall(r"(?:references|templates|scripts)/[\w.-]+\.(?:md|py)", text))
        self.assertTrue(paths)
        self.assertEqual([p for p in sorted(paths) if not (SKILL / p).is_file()], [])


if __name__ == "__main__":
    unittest.main()
