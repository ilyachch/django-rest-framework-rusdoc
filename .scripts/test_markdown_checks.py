import unittest

import check_blank_lines
import check_code_language
import check_dashes
import check_headings
import check_paragraphs
import check_quotes


class MarkdownChecksTest(unittest.TestCase):
    def test_paragraphs_and_blocks(self):
        text = '# Title\n\nFirst line\nsecond line\n\n- list item\n  continuation\n\n```python\ncode\nmore code\n```\n'
        self.assertEqual([n for n, _ in check_paragraphs.check(text)], [4, 7])
        self.assertEqual(list(check_paragraphs.check('One line\n\nAnother line\n')), [])
        self.assertEqual([n for n, _ in check_paragraphs.check('> first\n> second\n')], [2])

    def test_headings(self):
        text = '# One\n### Skipped\n#### Four\n## Back\n```python\n###### code\n```\n#### Skipped\n'
        self.assertEqual([n for n, _ in check_headings.check(text)], [2, 8])
        self.assertEqual([n for n, _ in check_headings.check('# One\n\nTitle\n---\n')], [])

    def test_code_language(self):
        text = '```python\n```\n~~~\ntext\n~~~\n````text\n```\n````\n'
        self.assertEqual([n for n, _ in check_code_language.check(text)], [3])

    def test_quotes_dashes_and_blank_lines_include_code(self):
        text = '```text\n«x» — y\n\n \n```\n'
        self.assertEqual([n for n, _ in check_quotes.check(text)], [2])
        self.assertEqual([n for n, _ in check_dashes.check(text)], [2])
        self.assertEqual([n for n, _ in check_blank_lines.check(text)], [4])
        self.assertEqual(list(check_blank_lines.check('a\n\nb\n')), [])

    def test_frontmatter_and_comments(self):
        text = '<!-- marker -->\n---\ntitle: Test\nother: Value\n---\n# Title\n'
        self.assertEqual(list(check_paragraphs.check(text)), [])
        self.assertEqual(list(check_headings.check(text)), [])


if __name__ == '__main__':
    unittest.main()
