#!/usr/bin/env python3
"""Find consecutive blank lines in Markdown files."""
from markdown_common import run


def check(text):
    blank = False
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            if blank:
                yield number, 'несколько пустых строк подряд'
            blank = True
        else:
            blank = False


if __name__ == '__main__':
    raise SystemExit(run(check))
