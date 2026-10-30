#!/usr/bin/env python3
"""Find fenced code blocks without a language label."""
from markdown_common import FENCE, markdown_lines, run


def check(text):
    for number, line, kind in markdown_lines(text):
        if kind == 'fence' and not FENCE.match(line).group(2).strip():
            yield number, 'не указан язык блока кода'


if __name__ == '__main__':
    raise SystemExit(run(check))
