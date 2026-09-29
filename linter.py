import json
import os.path
import re
import sublime

from SublimeLinter.lint import Linter


# `NaN`, `Infinity` and `-Infinity` are not JSON (RFC 8259) but Python's
# decoder accepts them by default. Strings are matched too so that we can skip
# over them when looking for the position.
NON_JSON_CONSTANT_RE = re.compile(r'"(?:[^"\\]|\\.)*"|(?P<constant>-?Infinity|NaN)')


class NonJSONConstant(ValueError):
    pass


def reject_constant(name):
    raise NonJSONConstant(name)


def describe_non_json_constant(code, name):
    """Return an error message, in the format `strict_regex` expects, for the first `name` in `code`."""
    # Only done on the error path, so valid documents don't pay for it.
    for match in NON_JSON_CONSTANT_RE.finditer(code):
        if match.group('constant') == name:
            start = match.start()
            line = code.count('\n', 0, start) + 1
            col = start - (code.rfind('\n', 0, start) + 1) + 1
            return '{} is not valid JSON: line {} column {}'.format(name, line, col)

    return '{} is not valid JSON: line 1 column 1'.format(name)


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
                json.loads(code, parse_constant=reject_constant)
            else:
                self.regex = self.loose_regex
                sublime.decode_value(code)

            return ''
        except NonJSONConstant as err:
            return describe_non_json_constant(code, str(err))
        except ValueError as err:
            return str(err)
