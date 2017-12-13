#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2015-2016 The SublimeLinter Community
# Copyright (c) 2013-2014 Aparajita Fishman
#
# License: MIT
#

"""This module exports the JSON plugin linter class."""

import json
import os.path
import re
import sublime

from SublimeLinter.lint import Linter


class JSON(Linter):
    """Provides an interface to json.loads()."""

    syntax = 'json'
    cmd = None
    loose_regex = re.compile(r'^.+: (?P<message>.+) in \(data\):(?P<line>\d+):(?P<col>\d+)')
    strict_regex = re.compile(r'^(?P<message>.+):\s*line (?P<line>\d+) column (?P<col>\d+)')
    regex = loose_regex
    defaults = {
        'strict': True
    }

    extensions = [
        '.sublime-build',
        '.sublime-color-scheme',
        '.sublime-commands',
        '.sublime-completions',
        '.sublime-keymap',
        '.sublime-menu',
        '.sublime_metrics',
        '.sublime-mousemap',
        '.sublime-project',
        '.sublime_session',
        '.sublime-settings',
        '.sublime-theme',
        '.sublime-workspace',
    ]

    def run(self, cmd, code):
        """
        Attempt to parse code as JSON.

        Returns '' if it succeeds, the error message if it fails.
        Use ST's loose parser for its setting files, or when specified.
        """
        is_sublime_file = os.path.splitext(self.filename)[1] in self.extensions

        if Linter.get_view_settings(self).get('strict') and not is_sublime_file:
            strict = True
        else:
            strict = False

        try:
            if strict:
                self.__class__.regex = self.strict_regex
                json.loads(code)
            else:
                self.__class__.regex = self.loose_regex
                sublime.decode_value(code)

            return ''
        except ValueError as err:
            return str(err)
