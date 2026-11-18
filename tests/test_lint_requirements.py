import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/business-analysis"
FIXTURES = ROOT / "tests/fixtures"

sys.path.insert(0, str(SKILL / "scripts"))
import lint_requirements as lr


def _write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def write_tmp(text):
    fd, name = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    _write(Path(name), text)
    return name


def run(**files):
    with tempfile.TemporaryDirectory() as td:
        paths = []
        for name, text in files.items():
            path = Path(td) / name
            _write(path, text)
            paths.append(str(path))
        return lr.lint(paths)


class LintRequirementsTest(unittest.TestCase):
    def test_good_fixture_clean(self):
        self.assertEqual(lr.lint([str(FIXTURES / "good.md")]), [])

    def test_duplicate_id_across_files(self):
        f = run(a="- **FR-001**: x\n- **FR-001.AC1**: Given a When b Then c\n",
                b="- **FR-001**: y\n- **FR-001.AC1**: Given a When b Then c\n")
        self.assertEqual([x.rule for x in f], ["duplicate-id", "duplicate-id"])

    def test_missing_ac(self):
        f = run(a="- **FR-001**: The system shall log refunds\n")
        self.assertEqual([(x.rule, x.line) for x in f], [("missing-ac", 1)])

    def test_dangling_ac_parent_and_br_cite(self):
        f = run(a="- **FR-001**: refund [BR-009]\n- **FR-001.AC1**: Given a When b Then c\n- **FR-007.AC1**: Given a When b Then c\n")
        self.assertEqual(sorted(x.rule for x in f), ["dangling-ref", "dangling-ref"])

    def test_cross_file_citation_resolves(self):
        brd = "- **FR-002**: x\n- **FR-002.AC1**: Given a When b Then c\n"
        self.assertEqual(run(brd=brd, gap="Gap closes FR-002.\n"), [])
        self.assertEqual([x.rule for x in run(gap="Gap closes FR-002.\n")], ["dangling-ref"])

    def test_orphan_br(self):
        f = run(a="- **BR-001**: Refunds within 30 days\n")
        self.assertEqual([x.rule for x in f], ["orphan-br"])

    def test_fenced_code_ignored(self):
        f = run(a="```mermaid\nflowchart LR\n FR-001 --> FR-009\n```\n- **FR-001**: x\n- **FR-001.AC1**: Given a When b Then c\n")
        self.assertEqual(f, [])

    def test_crlf_and_bom_parse_same(self):
        text = (FIXTURES / "good.md").read_text(encoding="utf-8")
        self.assertEqual(run(a="\ufeff" + text.replace("\n", "\r\n")), [])

    def test_empty_and_no_id_files_clean(self):
        self.assertEqual(run(a="", b="# Notes\nNothing here.\n"), [])

    def test_vague_term_en(self):
        f = run(a="- **FR-001**: Refunds must be fast and user-friendly\n- **FR-001.AC1**: Given a When b Then c\n")
        self.assertEqual([x.rule for x in f], ["vague-term", "vague-term"])
        self.assertTrue(any("'fast'" in x.message for x in f))

    def test_vague_term_word_boundary(self):
        f = run(a="- **FR-001**: Breakfast menu shows Simplex items\n- **FR-001.AC1**: Given a When b Then c\n")
        self.assertEqual(f, [])
        f = run(a="- **FR-001**: Show items etc.\n- **FR-001.AC1**: Given a When b Then c and/or d\n")
        self.assertEqual(len(f), 2)

    def test_vague_term_only_in_definition_blocks(self):
        self.assertEqual(run(a="## Assumptions\n- A-01: fast network\n"), [])

    def test_vague_term_vietnamese(self):
        f = run(a="- **FR-001**: Hệ thống xử lý nhanh, giao diện thân thiện\n- **FR-001.AC1**: Given a When b Then c\n")
        self.assertEqual(len(f), 2)

    def test_vague_term_vietnamese_nfd(self):
        import unicodedata
        text = unicodedata.normalize("NFD", "- **FR-001**: Giao diện thân thiện\n- **FR-001.AC1**: Given a When b Then c\n")
        self.assertEqual([x.rule for x in run(a=text)], ["vague-term"])

    def test_unmeasurable_nfr(self):
        f = run(a="| NFR-001 | Page loads quickly enough |\n- **NFR-001.AC1**: Given load When open Then page is responsive\n")
        self.assertIn("unmeasurable-nfr", [x.rule for x in f])
        f = run(a="| NFR-001 | p95 page load < 2 s |\n- **NFR-001.AC1**: Given 100 users When open Then p95 < 2 s\n")
        self.assertEqual(f, [])

    def test_cli_exit_codes(self):
        good = str(FIXTURES / "good.md")
        bad = write_tmp("- **FR-001**: The system shall log refunds\n")
        with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()):
            self.assertEqual(lr.main([]), 2)
            self.assertEqual(lr.main(["/nonexistent.md"]), 2)
            self.assertEqual(lr.main([good]), 0)
        self.assertEqual(out.getvalue(), "")
        with redirect_stdout(io.StringIO()) as out, redirect_stderr(io.StringIO()):
            self.assertEqual(lr.main([bad]), 1)
        self.assertEqual(out.getvalue().splitlines(),
                         [f"{bad}:1: missing-ac: FR-001 has no acceptance criteria"])


if __name__ == "__main__":
    unittest.main()
