#!/usr/bin/env python3
"""Find em dashes in Markdown files."""
from markdown_common import run


def check(text):
    for number, line in enumerate(text.splitlines(), 1):
        if '—' in line:
            yield number, 'длинное тире недопустимо'


if __name__ == '__main__':
    raise SystemExit(run(check))
