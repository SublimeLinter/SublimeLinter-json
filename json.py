#
# json.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
#
# Project: https://github.com/SublimeLinter/SublimeLinter-contrib-json
# License: MIT
#

"""This module exports the JSON plugin linter class."""

import json

from SublimeLinter.lint import Linter


class JSON(Linter):

    """Provides an interface to json.loads()."""

    language = 'json'
    cmd = None
    regex = r'^(?P<message>.+):\s*line (?P<line>\d+) column (?P<col>\d+)'

    def run(self, cmd, code):
        """Attempt to parse code as JSON, return '' if it succeeds, the error message if it fails."""
        try:
            json.loads(code)
            return ''
        except ValueError as err:
            return str(err)
