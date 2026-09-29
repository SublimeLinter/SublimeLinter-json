import importlib
import unittest
from unittest import mock

import sublime


LinterModule = importlib.import_module('SublimeLinter-json.linter')
Linter = LinterModule.JSON


class TestConstants(unittest.TestCase):
    def lint(self, code, strict=True, filename='data.json'):
        # `filename` is a read-only property, and the view is a stand-in
        with mock.patch.object(Linter, 'filename', new_callable=mock.PropertyMock, return_value=filename):
            linter = Linter(sublime.View(0), {'strict': strict})
            output = linter.run(None, code)
            return output, list(linter.find_errors(output))

    def assertError(self, code, line, col, message_part):
        output, errors = self.lint(code)
        self.assertTrue(errors, 'no error for {!r} (output: {!r})'.format(code, output))
        self.assertEqual((errors[0]['line'], errors[0]['col']), (line, col))
        self.assertIn(message_part, errors[0]['message'])

    def test_valid_documents_still_pass(self):
        for code in ('{}', '[1, 2.5, -3e2, true, false, null]', '{"a": "NaN", "b": "Infinity"}'):
            output, errors = self.lint(code)
            self.assertEqual(output, '')
            self.assertFalse(errors)

    def test_nan(self):
        self.assertError('{"n": NaN}', 0, 6, 'NaN')

    def test_infinity(self):
        self.assertError('{"i": Infinity}', 0, 6, 'Infinity')

    def test_negative_infinity_points_at_the_minus_sign(self):
        self.assertError('[1, -Infinity]', 0, 4, 'Infinity')

    def test_position_on_a_later_line(self):
        self.assertError('{\n  "a": 1,\n  "b": NaN\n}', 2, 7, 'NaN')

    def test_constant_names_inside_strings_are_ignored_when_locating(self):
        self.assertError('["NaN", "-Infinity", NaN]', 0, 21, 'NaN')

    def test_ordinary_syntax_errors_are_unchanged(self):
        output, errors = self.lint('{"a": }')
        self.assertTrue(errors)
        self.assertIn('Expecting value', errors[0]['message'])

    def test_loose_mode_is_unchanged(self):
        # .sublime-* files use Sublime's own parser
        output, errors = self.lint('{"a": 1, // c\n}', filename='x.sublime-settings')
        self.assertEqual(output, '')
        self.assertFalse(errors)
