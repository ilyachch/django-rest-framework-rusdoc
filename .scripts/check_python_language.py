#!/usr/bin/env python3
"""Require the canonical python language label instead of py."""
from markdown_common import FENCE, markdown_lines, run


def check(text):
    for number, line, kind in markdown_lines(text):
        if kind == 'fence' and FENCE.match(line).group(2).strip().split()[:1] == ['py']:
            yield number, 'используйте python вместо py для языка блока кода'


if __name__ == '__main__':
    raise SystemExit(run(check))
