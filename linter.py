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

    # A locator miss has no trustworthy column; report it against the file.
    return '{} is not valid JSON: line 1'.format(name)


class DuplicateKey(ValueError):
    pass


def reject_duplicate_keys(pairs):
    """`object_pairs_hook` for `json.loads` that refuses objects with repeated keys."""
    obj = dict(pairs)
    if len(obj) != len(pairs):
        raise DuplicateKey()
    return obj


# Strings (so that we can skip over their content) and the structural characters.
TOKEN_RE = re.compile(r'"(?:[^"\\]|\\.)*"|[{}\[\],]')


def describe_duplicate_key(code):
    """Return an error message, in the format `strict_regex` expects, for the first duplicate key in `code`.

    Only used on the error path, when `reject_duplicate_keys` already found one, so
    valid documents don't pay for it. The decoder hook does not know positions, so
    we scan the tokens ourselves and track the keys seen per object.
    """
    stack = []  # one entry per open container: a set of keys for objects, None for arrays
    expect_key = False
    for match in TOKEN_RE.finditer(code):
        token = match.group(0)
        if token == '{':
            stack.append(set())
            expect_key = True
        elif token == '[':
            stack.append(None)
        elif token in ('}', ']'):
            if stack:
                stack.pop()
            expect_key = False
        elif token == ',':
            expect_key = bool(stack) and stack[-1] is not None
        elif expect_key and stack and stack[-1] is not None:
            key = json.loads(token)  # resolves escapes, `"a"` is the same key as `"a"`
            if key in stack[-1]:
                start = match.start()
                line = code.count('\n', 0, start) + 1
                col = start - (code.rfind('\n', 0, start) + 1) + 1
                return 'Duplicate key {}: line {} column {}'.format(token, line, col)
            stack[-1].add(key)
            expect_key = False

    # A locator miss has no trustworthy column; report it against the file.
    return 'Duplicate key: line 1'


class JSON(Linter):
    cmd = None
    loose_regex = re.compile(r'^.+: (?P<message>.+) in \(data\):(?P<line>\d+):(?P<col>\d+)')
    strict_regex = re.compile(r'^(?P<message>.+):\s*line (?P<line>\d+)(?: column (?P<col>\d+)|$)')
    regex = loose_regex
    defaults = {
        'selector': 'source.json',
        'strict': True,
        'check_duplicate_keys': True
    }

    def run(self, cmd, code):
        """
        Attempt to parse code as JSON.

        Returns '' if it succeeds, the error message if it fails.
        Use ST's loose parser for its setting files, or when specified.
        Duplicate keys are only checked in strict mode, and can be turned off with
        the `check_duplicate_keys` setting (it costs time on very large files, and
        some files use repeated keys on purpose).
        """
        is_sublime_file = os.path.splitext(self.filename)[1].startswith('.sublime-')

        if self.settings.get('strict') and not is_sublime_file:
            strict = True
        else:
            strict = False

        try:
            if strict:
                self.regex = self.strict_regex
                pairs_hook = reject_duplicate_keys if self.settings.get('check_duplicate_keys', True) else None
                json.loads(code, parse_constant=reject_constant, object_pairs_hook=pairs_hook)
            else:
                self.regex = self.loose_regex
                sublime.decode_value(code)

            return ''
        except NonJSONConstant as err:
            return describe_non_json_constant(code, str(err))
        except DuplicateKey:
            return describe_duplicate_key(code)
        except ValueError as err:
            return str(err)
