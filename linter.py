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

    line_comment_regex = re.compile(r'\s*//.*')
    block_comment_regex = re.compile(r'\s*/\*.*?\*/', flags=re.DOTALL)

    def run(self, cmd, code):
        """Attempt to parse code as JSON, return '' if it succeeds, the error message if it fails."""

        # Ignore comments in .sublime-settings files.
        if os.path.splitext(self.filename)[1] == '.sublime-settings':
            code = self.line_comment_regex.sub('', code)
            code = self.block_comment_regex.sub('', code)

        try:
            json.loads(code)
            return ''
        except ValueError as err:
            return str(err)
