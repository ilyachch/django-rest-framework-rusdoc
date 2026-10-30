"""Shared command-line and Markdown block helpers for the checks."""

import argparse
import re
import sys
from pathlib import Path

FENCE = re.compile(r'^ *(`{3,}|~{3,})(.*)$')
HEADING = re.compile(r'^ {0,3}(#{1,6})(?:\s|$)')
SETEXT = re.compile(r'^ {0,3}(=+|-+)\s*$')
LIST = re.compile(r'^\s*(?:[-+*]|\d+[.)])\s+')
RULE = re.compile(r'^ {0,3}(?:(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,})$')


def markdown_lines(text):
    """Yield (line number, line, kind), skipping fenced code and front matter."""
    fence = None
    frontmatter = False
    can_start_frontmatter = True
    comment = False
    for number, line in enumerate(text.splitlines(), 1):
        if can_start_frontmatter and line.strip() == '---':
            frontmatter = True
            can_start_frontmatter = False
            yield number, line, 'other'
            continue
        if frontmatter:
            if line.strip() in ('---', '...'):
                frontmatter = False
            yield number, line, 'other'
            continue
        if can_start_frontmatter and line.strip() and not line.lstrip().startswith('<!--'):
            can_start_frontmatter = False
        if fence:
            if re.match(r'^ *' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*$', line):
                fence = None
            yield number, line, 'code'
            continue
        match = FENCE.match(line)
        if match:
            fence = match.group(1)
            yield number, line, 'fence'
            continue
        if comment:
            if '-->' in line:
                comment = False
            yield number, line, 'other'
            continue
        if line.lstrip().startswith('<!--'):
            comment = '-->' not in line
            yield number, line, 'other'
            continue
        yield number, line, 'text'


def run(check):
    parser = argparse.ArgumentParser(description=check.__doc__)
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    failed = False
    for filename in args.files:
        try:
            content = Path(filename).read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            print(f'{filename}: {exc}', file=sys.stderr)
            failed = True
            continue
        for number, message in check(content):
            print(f'{filename}:{number}: {message}')
            failed = True
    return int(failed)
