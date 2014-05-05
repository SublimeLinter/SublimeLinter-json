#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2013 Aparajita Fishman
#
# License: MIT
#

"""This module exports the JSON plugin linter class."""

import json
import os.path
import re

from SublimeLinter.lint import Linter


class JSON(Linter):

    """Provides an interface to json.loads()."""

    syntax = 'json'
    cmd = None
    regex = r'^(?P<message>.+):\s*line (?P<line>\d+) column (?P<col>\d+)'

    line_comment_re = re.compile(r'[ \t]*//.*')
    block_comment_re = re.compile(r'/\*(.*?)\*/', re.DOTALL)
    inner_re = re.compile(r'^([^\r\n]*?(\r?\n|$))', re.MULTILINE)
    extensions = [
        '.sublime-build',
        '.sublime-commands',
        '.sublime-completions',
        '.sublime-keymap',
        '.sublime-menu',
        '.sublime-mousemap',
        '.sublime-project',
        '.sublime-settings',
        '.sublime-workspace',
    ]

    @classmethod
    def strip_comment(cls, match):
        """Return a block comment stripped of all content on each line, but leaving the EOL."""
        inner = cls.inner_re.sub(r'\2', match.group(1))
        return inner

    def run(self, cmd, code):
        """Attempt to parse code as JSON, return '' if it succeeds, the error message if it fails."""

        # Ignore comments in .sublime-* files.
        if os.path.splitext(self.filename)[1] in self.extensions:
            code = self.line_comment_re.sub('', code)
            code = self.block_comment_re.sub(self.strip_comment, code)

        try:
            json.loads(code)
            return ''
        except ValueError as err:
            return str(err)
