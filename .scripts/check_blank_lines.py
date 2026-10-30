#!/usr/bin/env python3
"""Find consecutive blank lines outside fenced code blocks."""
from markdown_common import markdown_lines, run


def check(text):
    blank = False
    for number, line, kind in markdown_lines(text):
        if kind == 'code':
            blank = False
            continue
        if not line.strip():
            if blank:
                yield number, 'несколько пустых строк подряд'
            blank = True
        else:
            blank = False


if __name__ == '__main__':
    raise SystemExit(run(check))
