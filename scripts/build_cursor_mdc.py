#!/usr/bin/env python3
"""Build rust-design-patterns-cursor.mdc: a zip of Cursor Project Rules.

Converts skills/*/SKILL.md into one Rule per skill, flat under rules/ inside
the zip (rules/<skill>.mdc) so Cursor discovers each without an extra
subdirectory. A skill's references/ (if any) is bundled alongside at
rules/<skill>/references/. Relative links inside a rule body are rewritten
for that flat layout: `references/...` -> `<skill>/references/...` for a
skill's own references, and `../other-skill/references/...` /
`../other-skill/SKILL.md` -> `other-skill/references/...` / `other-skill.mdc`
for links to a sibling skill.

To install manually: unzip into a project's `.cursor/` directory.
"""
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DEFAULT_OUT = REPO_ROOT / "starrocks-cursor.mdc"


def parse_skill(path):
    text = path.read_text(encoding="utf-8")
    end = text.index("\n---\n", 4)
    front, body = text[4:end], text[end + 5 :].lstrip("\n")
    meta = {}
    for line in front.splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip('"')
    return meta, body


def rule_body(skill_name, body):
    body = body.replace("`references/", f"`{skill_name}/references/")
    for other in SKILLS_DIR.iterdir():
        if other.name == skill_name:
            continue
        body = body.replace(f"../{other.name}/references/", f"{other.name}/references/")
        body = body.replace(f"../{other.name}/SKILL.md", f"{other.name}.mdc")
    return body


def add_skill(zf, skill_dir):
    name = skill_dir.name
    meta, body = parse_skill(skill_dir / "SKILL.md")
    mdc = (
        "---\n"
        f"description: {meta['description']}\n"
        'globs: ["**/*.rs"]\n'
        "alwaysApply: false\n"
        "---\n\n"
        f"{rule_body(name, body)}"
    )
    zf.writestr(f"rules/{name}.mdc", mdc)

    references = skill_dir / "references"
    if references.is_dir():
        for path in references.rglob("*"):
            if path.is_file():
                rel = path.relative_to(references).as_posix()
                zf.write(path, f"rules/{name}/references/{rel}")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    out.unlink(missing_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for skill_dir in sorted(SKILLS_DIR.iterdir()):
            if (skill_dir / "SKILL.md").is_file():
                add_skill(zf, skill_dir)


if __name__ == "__main__":
    main()
