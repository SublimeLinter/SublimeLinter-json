import json
import os.path
import re
import sublime

from SublimeLinter.lint import Linter


class JSON(Linter):
    cmd = None
    loose_regex = re.compile(r'^.+: (?P<message>.+) in \(data\):(?P<line>\d+):(?P<col>\d+)')
    strict_regex = re.compile(r'^(?P<message>.+):\s*line (?P<line>\d+) column (?P<col>\d+)')
    regex = loose_regex
    defaults = {
        'selector': 'source.json',
        'strict': True
    }

    def run(self, cmd, code):
        """
        Attempt to parse code as JSON.

        Returns '' if it succeeds, the error message if it fails.
        Use ST's loose parser for its setting files, or when specified.
        """
        is_sublime_file = os.path.splitext(self.filename)[1].startswith('.sublime-')

        if self.settings.get('strict') and not is_sublime_file:
            strict = True
        else:
            strict = False

        try:
            if strict:
                self.regex = self.strict_regex
                json.loads(code)
            else:
                self.regex = self.loose_regex
                sublime.decode_value(code)

            return ''
        except ValueError as err:
            return str(err)
