"""Structural lint for business-analysis requirement IDs in Markdown docs."""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from dataclasses import dataclass

ID_RE = r"\b(BR|FR|NFR)-(\d{3,})(?:\.AC(\d+))?\b"

_ID_PATTERN = re.compile(ID_RE)
_DEF_PATTERN = re.compile(
    r"^\s*(?:#{1,6}\s+|[-*+]\s+|\|\s*)?(?:\*\*)?(?P<id>" + ID_RE + r")(?:\*\*)?\s*[:|]"
)
_FENCE_RE = re.compile(r"^\s*```")
_HEADING_RE = re.compile(r"^\s*#{1,6}\s+")
_TABLE_RE = re.compile(r"^\s*\|")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.message}"


@dataclass
class Block:
    id: str
    kind: str  # "BR" | "FR" | "NFR" | "AC"
    path: str
    line: int
    text: str  # definition line + continuation lines


def _kind_of(id: str) -> str:
    if ".AC" in id:
        return "AC"
    return id.split("-", 1)[0]


def _base_id(id: str) -> str:
    return id.split(".", 1)[0]


def _read_lines(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8-sig") as f:
        return [line.rstrip("\n") for line in f]


def _add_citations(line, path, lineno, block_kind, skip, out):
    for m in _ID_PATTERN.finditer(line):
        if skip is not None and (m.start(), m.end()) == skip:
            continue
        out.append((m.group(0), path, lineno, block_kind))


def _scan_files(paths):
    blocks: list[Block] = []
    citations: list[tuple[str, str, int, str | None]] = []

    for path in paths:
        lines = _read_lines(path)
        in_fence = False
        current: dict | None = None

        for lineno, line in enumerate(lines, 1):
            if _FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            m = _DEF_PATTERN.match(line)
            if m:
                block_id = m.group("id")
                kind = _kind_of(block_id)
                current = {
                    "id": block_id,
                    "kind": kind,
                    "path": path,
                    "line": lineno,
                    "lines": [line],
                }
                blocks.append(current)
                _add_citations(
                    line, path, lineno, kind, (m.start("id"), m.end("id")), citations
                )
                continue

            if line.strip() == "":
                current = None
                continue

            if _HEADING_RE.match(line) or _TABLE_RE.match(line):
                current = None
                _add_citations(line, path, lineno, None, None, citations)
                continue

            block_kind = current["kind"] if current is not None else None
            if current is not None:
                current["lines"].append(line)
            _add_citations(line, path, lineno, block_kind, None, citations)

    out_blocks = [
        Block(
            id=b["id"],
            kind=b["kind"],
            path=b["path"],
            line=b["line"],
            text="\n".join(b["lines"]),
        )
        for b in blocks
    ]
    return out_blocks, citations


def parse(paths: list[str]) -> tuple[list[Block], list[tuple[str, str, int]]]:
    blocks, citations = _scan_files(paths)
    return blocks, [(id, path, line) for (id, path, line, _) in citations]


def lint(paths: list[str]) -> list[Finding]:
    blocks, citations = _scan_files(paths)
    findings: list[Finding] = []

    defined: dict[str, Block] = {}
    for b in blocks:
        if b.id in defined:
            first = defined[b.id]
            findings.append(
                Finding(
                    b.path,
                    b.line,
                    "duplicate-id",
                    f"{b.id} is defined more than once (first at {first.path}:{first.line})",
                )
            )
        else:
            defined[b.id] = b

    ac_defs: dict[str, list[Block]] = defaultdict(list)
    for b in blocks:
        if b.kind == "AC":
            ac_defs[_base_id(b.id)].append(b)

    for b in blocks:
        if b.kind in ("FR", "NFR") and not ac_defs.get(b.id):
            findings.append(
                Finding(b.path, b.line, "missing-ac", f"{b.id} has no acceptance criteria")
            )

    for b in blocks:
        if b.kind == "AC":
            base = _base_id(b.id)
            if base not in defined:
                findings.append(
                    Finding(b.path, b.line, "dangling-ref", f"{base} is not defined")
                )

    for cid, cpath, cline, _ in citations:
        if cid not in defined:
            findings.append(Finding(cpath, cline, "dangling-ref", f"{cid} is not defined"))

    cited_br: set[str] = set()
    for cid, _, _, block_kind in citations:
        if block_kind in ("FR", "NFR", "AC") and cid.startswith("BR-"):
            cited_br.add(cid)

    for b in blocks:
        if b.kind == "BR" and b.id not in cited_br:
            findings.append(
                Finding(b.path, b.line, "orphan-br", f"{b.id} is not cited by any requirement")
            )

    path_order = {path: i for i, path in enumerate(paths)}
    findings.sort(key=lambda f: (path_order.get(f.path, len(paths)), f.line, f.rule))
    return findings


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("usage: lint_requirements.py FILE.md [FILE.md ...]", file=sys.stderr)
        return 2
    try:
        findings = lint(argv)
    except (OSError, UnicodeDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    for finding in findings:
        print(finding.format())
    print(f"{len(findings)} finding(s) in {len(argv)} file(s)", file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
