#
# json.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
#
# Project: https://github.com/SublimeLinter/SublimeLinter-contrib-json
# License: MIT
#

import json

from SublimeLinter.lint import Linter


class JSON(Linter):
    language = 'json'
    cmd = None
    regex = r'^(?P<error>.+):\s*line (?P<line>\d+) column (?P<col>\d+)'

    def run(self, cmd, code):
        try:
            json.loads(code)
        except ValueError as err:
            return str(err)

        return ''
