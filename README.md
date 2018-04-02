SublimeLinter-json
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-json.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-json)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to the [JSON parser](http://docs.python.org/3/library/json.html?highlight=json.loads#json.loads) built into Sublime Text.
It will be used with files that have the "JSON" syntax.

To facilitate editing Sublime Text settings files, which may contain comments, this linter allows line comments (//) and multiline block comments (`/* */`), but they may not appear at the end of a line (after JSON data).


## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.


## Settings

This linter accepts a `"strict"` setting, which if false uses Sublime Text's "loose" parser so that trailing comma's and comments are accepted.

```json
"linters": {
	"json": {
		"strict": false
	}
}
```

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html
