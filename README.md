SublimeLinter-json
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-json.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-json)

This linter plugin for [SublimeLinter](http://sublimelinter.readthedocs.org) provides an interface to the [JSON parser](http://docs.python.org/3/library/json.html?highlight=json.loads#json.loads) built into Sublime Text. It will be used with files that have the “JSON” syntax.

To facilitate editing Sublime Text settings files, which may contain comments, this linter allows line comments (//) and multiline block comments (`/* */`), but they may not appear at the end of a line (after JSON data).

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here](http://sublimelinter.readthedocs.org/en/latest/installation.html).

Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin. 

## Settings

This linter accepts a `"strict"` setting, which if false uses Sublime Text's "loose" parser so that trailing comma's and comments are accepted.

```json
"linters": {
	"json": {
		"strict": false
	}
}
```

For general information on how SublimeLinter works with settings, please see [Settings](http://sublimelinter.readthedocs.org/en/latest/settings.html). For information on generic linter settings, please see [Linter Settings](http://sublimelinter.readthedocs.org/en/latest/linter_settings.html).
