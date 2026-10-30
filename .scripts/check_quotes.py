#!/usr/bin/env python3
"""Find guillemets in Markdown files."""
from markdown_common import run


def check(text):
    for number, line in enumerate(text.splitlines(), 1):
        if '«' in line or '»' in line:
            yield number, 'кавычки-ёлочки недопустимы'


if __name__ == '__main__':
    raise SystemExit(run(check))
