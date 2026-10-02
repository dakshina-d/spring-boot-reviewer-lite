"""Validate this package's intentionally small frontmatter subset and local links.

Standard library only. Does not run the reviewed application or call an AI model.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'spring-boot-reviewer-lite'


def validate():
    errors = []
    required = [
        SKILL / 'SKILL.md', SKILL / 'agents/openai.yaml',
        SKILL / 'references/review-checklist.md',
        SKILL / 'references/report-format.md',
        ROOT / 'README.md', ROOT / 'LICENSE',
        ROOT / 'examples/sample-review.md', ROOT / 'evals/README.md',
        ROOT / 'docs/COMPATIBILITY.md', ROOT / 'docs/TESTING.md',
        ROOT / 'portable/spring-boot-reviewer-lite.md',
        ROOT / 'tools/install.py', ROOT / 'tools/build_portable.py',
    ]
    for path in required:
        if not path.is_file():
            errors.append(f'Missing {path.relative_to(ROOT)}')
    if (SKILL / 'SKILL.md').is_file():
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append('SKILL.md needs opening and closing YAML delimiters')
        else:
            fields = {}
            for line in parts[1].strip().splitlines():
                key, sep, value = line.partition(':')
                if not sep or key not in {'name', 'description'} or key in fields:
                    errors.append(f'Invalid/duplicate frontmatter key: {key}')
                fields[key] = value.strip()
            if fields.get('name') != SKILL.name:
                errors.append('Skill name must match its folder')
            if not 1 <= len(fields.get('description', '')) <= 1024:
                errors.append('Description must contain 1–1024 characters')
            if len(parts[2].splitlines()) >= 500:
                errors.append('Keep SKILL.md body below 500 lines')
    for path in ROOT.rglob('*.md'):
        if any(part in {'.git', '__pycache__', '.agents', '.claude', '.kiro'} for part in path.relative_to(ROOT).parts):
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', path.read_text(encoding='utf-8')):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                continue
            local = target.split('#', 1)[0]
            if local and not (path.parent / local).exists():
                errors.append(f'{path.relative_to(ROOT)}: broken link {target}')
    return errors


if __name__ == '__main__':
    problems = validate()
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        raise SystemExit(1)
    print('PASS: required files, skill metadata, and local Markdown links')
