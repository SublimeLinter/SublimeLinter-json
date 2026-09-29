import importlib
import unittest
from unittest import mock

import sublime


LinterModule = importlib.import_module('SublimeLinter-json.linter')
Linter = LinterModule.JSON


class TestDuplicateKeys(unittest.TestCase):
    def lint(self, code, strict=True, filename='data.json'):
        # `filename` is a read-only property, and the view is a stand-in
        with mock.patch.object(Linter, 'filename', new_callable=mock.PropertyMock, return_value=filename):
            linter = Linter(sublime.View(0), {'strict': strict})
            output = linter.run(None, code)
            return output, list(linter.find_errors(output))

    def assertDuplicate(self, code, line, col, key):
        output, errors = self.lint(code)
        self.assertTrue(errors, 'no error for {!r} (output: {!r})'.format(code, output))
        self.assertEqual((errors[0]['line'], errors[0]['col']), (line, col))
        self.assertIn('Duplicate key', errors[0]['message'])
        self.assertIn(key, errors[0]['message'])

    def assertClean(self, code):
        output, errors = self.lint(code)
        self.assertEqual(output, '')
        self.assertFalse(errors)

    def test_top_level_duplicate_points_at_the_second_key(self):
        self.assertDuplicate('{"a": 1, "a": 2}', 0, 9, '"a"')

    def test_nested_duplicate_on_a_later_line(self):
        self.assertDuplicate('{"a": 1,\n  "b": {"c": 1, "c": 2}}', 1, 16, '"c"')

    def test_duplicate_in_an_object_inside_an_array(self):
        self.assertDuplicate('{"a": {"a": 1}, "b": [{"a": 1, "a": 2}]}', 0, 31, '"a"')

    def test_escaped_spelling_of_the_same_key(self):
        self.assertDuplicate('{"a": 1, "\\u0061": 2}', 0, 9, 'u0061')

    def test_key_appearing_in_a_string_value_is_not_a_duplicate(self):
        self.assertClean('{"k": "a", "l": "a", "a": 1}')

    def test_same_key_in_different_objects_is_fine(self):
        self.assertClean('[{"a": 1}, {"a": 2}, {"a": {"a": 3}}]')

    def test_closing_brace_inside_a_string_does_not_confuse_the_scan(self):
        self.assertDuplicate('{"x": "}", "x": 1}', 0, 11, '"x"')

    def test_valid_documents_still_pass(self):
        for code in ('{}', '[]', '{"a": 1, "b": [1, 2, {"c": null}]}'):
            self.assertClean(code)

    def test_ordinary_syntax_errors_are_unchanged(self):
        output, errors = self.lint('{"a": }')
        self.assertTrue(errors)
        self.assertIn('Expecting value', errors[0]['message'])

    def test_loose_mode_is_unchanged(self):
        # .sublime-* files use Sublime's own parser, which is not asked about duplicates
        output, errors = self.lint('{"a": 1, "a": 2}', filename='x.sublime-settings')
        self.assertEqual(output, '')
        self.assertFalse(errors)
