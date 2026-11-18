import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/business-analysis"

sys.path.insert(0, str(SKILL / "scripts"))
import lint_requirements as lr  # noqa: F401


def mermaid_blocks(*dirs):
    blocks = []
    for directory in dirs:
        for path in sorted(Path(directory).glob("*.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            in_mermaid = False
            current = None
            for line in lines:
                if line.strip() == "```mermaid":
                    in_mermaid = True
                    current = []
                    continue
                if in_mermaid and line.strip() == "```":
                    in_mermaid = False
                    blocks.append((path, current))
                    current = None
                    continue
                if in_mermaid:
                    current.append(line)
            if in_mermaid:
                raise ValueError(f"unclosed ```mermaid fence in {path}")
    return blocks


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
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 300)

    def test_requirement_templates_lint_clean(self):
        for name in ("requirements.md", "brd.md"):
            self.assertEqual(lr.lint([str(SKILL / "templates" / name)]), [], name)

    def test_requirement_templates_define_ids(self):
        for name in ("requirements.md", "brd.md"):
            blocks, _ = lr.parse([str(SKILL / "templates" / name)])
            kinds = {block.kind for block in blocks}
            self.assertTrue({"BR", "FR", "NFR", "AC"} <= kinds, (name, sorted(kinds)))

    def test_process_templates_define_no_ids(self):
        for name in ("process-doc.md", "gap-analysis.md", "stakeholder-register.md"):
            blocks, _ = lr.parse([str(SKILL / "templates" / name)])
            self.assertEqual(blocks, [], name)

    def test_mermaid_blocks_well_formed(self):
        blocks = mermaid_blocks(SKILL / "references", SKILL / "templates")
        self.assertTrue(blocks)
        for path, lines in blocks:
            body = [line for line in lines if line.strip()]
            self.assertRegex(body[0], r"^\s*(flowchart|mindmap)\b", path)
            subs = [line for line in body if re.match(r"^\s*subgraph\b", line)]
            ends = [line for line in body if re.match(r"^\s*end\s*$", line)]
            self.assertEqual(len(subs), len(ends), path)
            for line in subs:
                self.assertRegex(line, r'^\s*subgraph\s+\w+\s*\["[^"]+"\]', path)

    def test_mermaid_blocks_rejects_unclosed_fence(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "broken.md"
            path.write_text("```mermaid\nflowchart LR\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                mermaid_blocks(directory)

    def test_skill_links_resolve(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        paths = set(re.findall(r"(?:references|templates|scripts)/[\w.-]+\.(?:md|py)", text))
        self.assertTrue(paths)
        self.assertEqual([p for p in sorted(paths) if not (SKILL / p).is_file()], [])


if __name__ == "__main__":
    unittest.main()
