"""Shared helpers for validate.py and build.py. Standard library only."""

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNBOOKS = ROOT / "runbooks"
SKILLS = ROOT / "skills"

AREAS = [
    "collection", "platform", "boot", "kernel", "memory",
    "storage", "network", "hardware", "cluster", "tracing",
]
FAMILIES = ["rhel", "sles", "debian"]
RELEASES = {
    "rhel8": "rhel", "rhel9": "rhel", "rhel10": "rhel",
    "sles15sp6": "sles", "sles15sp7": "sles", "sles16": "sles",
    "debian12": "debian", "debian13": "debian",
    "ubuntu2204": "debian", "ubuntu2404": "debian",
}
MODES = ["offline", "live", "both"]
RISKS = ["read-only", "intrusive", "disruptive"]
TAGS = ["unverified", "man", "lab"]
SECTIONS = ["When to use", "Check first", "Act", "Interpret", "Next", "Guardrails"]
SKILL_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def tokens(text):
    return math.ceil(len(text) / 3.5)


def split_front_matter(text):
    """Return (front_matter_text, body) or (None, text)."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5:]


def _scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_yaml_subset(text):
    """Parse `key: value`, inline `[a, b]` lists, and one-level nested maps."""
    data, errors, current = {}, [], None
    for raw in text.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw.startswith((" ", "\t"))
        if ":" not in raw:
            errors.append(f"unparseable front matter line: {raw!r}")
            continue
        key, _, value = raw.strip().partition(":")
        key = key.strip()
        if indented:
            if current is None or not isinstance(data.get(current), dict):
                errors.append(f"unexpected indented line: {raw!r}")
            else:
                data[current][key] = _scalar(value)
            continue
        current = key
        value = value.strip()
        if key in data:
            errors.append(f"duplicate key: {key}")
        if value == "":
            data[key] = {}
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_scalar(v) for v in inner.split(",")] if inner else []
        else:
            data[key] = _scalar(value)
    return data, errors


@dataclass
class Runbook:
    path: Path
    text: str
    fm: dict
    body: str
    errors: list = field(default_factory=list)

    @property
    def id(self):
        return self.fm.get("id", self.path.stem)

    @property
    def rel(self):
        return self.path.relative_to(ROOT).as_posix()


def load_runbook(path):
    text = path.read_text(encoding="utf-8")
    fm_text, body = split_front_matter(text)
    if fm_text is None:
        return Runbook(path, text, {}, text, ["missing or unterminated front matter"])
    fm, errors = parse_yaml_subset(fm_text)
    return Runbook(path, text, fm, body, errors)


def load_runbooks():
    return [load_runbook(p) for p in sorted(RUNBOOKS.glob("*/*.md"))]


def sections(body):
    """Map H2 title -> text, preserving order. Ignores fences when matching headings."""
    result, current, fenced = {}, None, False
    for line in body.split("\n"):
        if line.startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            current = line[3:].strip()
            result[current] = []
        elif current is not None:
            result[current].append(line)
    return {k: "\n".join(v).strip("\n") for k, v in result.items()}
