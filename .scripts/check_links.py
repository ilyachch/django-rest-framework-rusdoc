#!/usr/bin/env python3
"""Check Markdown link syntax, local files and heading anchors."""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_common import HEADING, SETEXT, markdown_lines


def anchor(title):
    """Generate an anchor from letters, hyphens and spaces."""
    title = re.sub(r'\s+#+\s*$', '', title)
    title = re.sub(r'!?(?:\[([^]]+)\])\([^)]*\)', r'\1', title)
    title = ''.join(c for c in title if c.isalpha() or c.isspace() or c == '-')
    return re.sub(r'\s+', '-', title.strip()).lower()


def anchors(text):
    result = set()
    previous = None
    for _, line, kind in markdown_lines(text):
        if kind != 'text':
            previous = None
            continue
        match = HEADING.match(line)
        if match:
            result.add(anchor(line[match.end():]))
            previous = None
        elif previous and SETEXT.match(line):
            result.add(anchor(previous))
            previous = None
        else:
            previous = line.strip() or None
    return result


def mask_inline_code(line):
    return re.sub(r'(`+)(.*?)(\1)', lambda m: ' ' * len(m.group()), line)


def check(text, path):
    cache = {}
    for number, line, kind in markdown_lines(text):
        if kind != 'text':
            continue
        line = mask_inline_code(line)
        # Handle balanced parentheses in link targets, including URLs with parentheses.
        pos = 0
        covered = []
        while pos < len(line):
            start = line.find('[', pos)
            if start < 0:
                break
            end = line.find(']', start + 1)
            if end < 0:
                break
            if end + 1 >= len(line) or line[end + 1] != '(':
                if end + 1 < len(line) and line[end + 1] in '[:':
                    yield number, 'ссылки должны использовать формат [текст](адрес)'
                pos = end + 1
                continue
            depth = 1
            stop = end + 2
            while stop < len(line) and depth:
                if line[stop] == '(' and (stop == 0 or line[stop - 1] != '\\'):
                    depth += 1
                elif line[stop] == ')' and (stop == 0 or line[stop - 1] != '\\'):
                    depth -= 1
                stop += 1
            if depth:
                yield number, 'незакрытая ссылка'
                break
            covered.append((start, stop))
            target = line[end + 2:stop - 1].strip()
            # Optional Markdown title, with either quoted or parenthesized syntax.
            target = re.sub(r'\s+(?:"[^"]*"|\'[^\']*\'|\([^)]*\))\s*$', '', target)
            if target.startswith('<') and target.endswith('>'):
                target = target[1:-1]
            try:
                url = urlsplit(target)
            except ValueError:
                yield number, f'некорректный адрес ссылки: {target}'
                pos = stop
                continue
            if url.scheme in ('http', 'https') and url.netloc:
                pass
            elif url.scheme or url.netloc or not target:
                yield number, f'ссылка должна вести на web или файл: {target}'
            else:
                local = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
                if not local.is_file():
                    yield number, f'файл ссылки не найден: {target}'
                elif url.fragment:
                    try:
                        if local not in cache:
                            cache[local] = anchors(local.read_text(encoding='utf-8'))
                        if unquote(url.fragment).lower() not in cache[local]:
                            yield number, f'якорь не найден: {target}'
                    except (OSError, UnicodeError) as exc:
                        yield number, f'не удалось прочитать цель ссылки {target}: {exc}'
            pos = stop
        remainder = list(line)
        for start, stop in covered:
            remainder[start:stop] = ' ' * (stop - start)
        if re.search(r'https?://[^\s<>]+', ''.join(remainder)):
            yield number, 'адрес должен быть оформлен как [текст](адрес)'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    failed = False
    for filename in args.files:
        path = Path(filename)
        try:
            text = path.read_text(encoding='utf-8')
            for number, message in check(text, path):
                print(f'{filename}:{number}: {message}')
                failed = True
        except (OSError, UnicodeError) as exc:
            print(f'{filename}: {exc}', file=sys.stderr)
            failed = True
    return int(failed)


if __name__ == '__main__':
    raise SystemExit(main())
