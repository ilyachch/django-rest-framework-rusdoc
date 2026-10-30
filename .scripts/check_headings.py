#!/usr/bin/env python3
"""Find skipped Markdown heading levels."""
from markdown_common import HEADING, SETEXT, markdown_lines, run


def check(text):
    previous_level = 0
    previous_text = None
    for number, line, kind in markdown_lines(text):
        if kind != 'text':
            previous_text = None
            continue
        heading = HEADING.match(line)
        setext = SETEXT.match(line) if previous_text else None
        if heading or setext:
            level = len(heading.group(1)) if heading else (1 if setext.group(1)[0] == '=' else 2)
            if previous_level and level > previous_level + 1:
                yield number if heading else previous_text, f'переход с заголовка {previous_level} на {level}'
            previous_level = level
            previous_text = None
        else:
            previous_text = number if line.strip() else None


if __name__ == '__main__':
    raise SystemExit(run(check))
