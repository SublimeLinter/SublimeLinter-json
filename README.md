SublimeLinter-json
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-json.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-json)

This linter plugin for [SublimeLinter](http://sublimelinter.readthedocs.org) provides an interface to the [JSON parser](http://docs.python.org/3/library/json.html?highlight=json.loads#json.loads) built into Sublime Text. It will be used with files that have the “JSON” syntax.

To facilitate editing Sublime Text settings files, which may contain comments, this linter allows line comments (//) and multiline block comments (/* */), but they may not appear at the end of a line (after JSON data).

## Installation
SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here](http://sublimelinter.readthedocs.org/en/latest/installation.html).

Please use [Package Control](https://sublime.wbond.net/installation) to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette](http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html) and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `json`. Among the entries you should see `SublimeLinter-json`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings
For general information on how SublimeLinter works with settings, please see [Settings](http://sublimelinter.readthedocs.org/en/latest/settings.html). For information on generic linter settings, please see [Linter Settings](http://sublimelinter.readthedocs.org/en/latest/linter_settings.html).

Settings are accessed via the <kbd>Preferences</kbd> > <kbd>Package Settings</kbd> > <kbd>SublimeLinter-json</kbd> menu.

### strict
If strict is set to true (default), linter will work in strict mode in which comments are not allowed. Otherwise, it will use a "soft" check which allows comments.

### strict_exceptions
A list of file extensions which are always checked in a non-strict manner. By default this includes .sublime-* extensions which often include comments.

## Contributing
If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.

Thank you for helping out!
