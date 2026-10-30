#!/usr/bin/env python3
"""Find Markdown paragraphs spanning multiple source lines."""
import re
from markdown_common import HEADING, LIST, RULE, SETEXT, markdown_lines, run


def check(text):
    paragraph = None
    for number, line, kind in markdown_lines(text):
        if kind != 'text' or not line.strip():
            paragraph = None
            continue
        if HEADING.match(line) or (paragraph is not None and SETEXT.match(line)):
            paragraph = None
            continue
        if line[:1].isspace() or LIST.match(line) or line.startswith('>'):
            paragraph = None
            continue
        if (RULE.match(line)
                or line.lstrip().startswith('|') or re.match(r'^\s*\[[^]]+\]:', line)
                or re.match(r'^ {0,3}</?[A-Za-z][\w-]*(?:\s|/?>)', line)):
            paragraph = None
            continue
        if paragraph is not None:
            yield number, f'многострочный абзац (начало: строка {paragraph})'
        else:
            paragraph = number


if __name__ == '__main__':
    raise SystemExit(run(check))
