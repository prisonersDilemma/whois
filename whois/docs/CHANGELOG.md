#===============================================================================
# config.py changes:
* Changed the name of the logger to __name__ (the file) from __package__, in
  order to implement more loggers.
* Added first version of set_option function. Haven't tested, yet. Only sets
  option in the config, doesn't rewrite the current file in place. Not sure
  how to go about that; they should really be two different things.
* Doubled defaults of bufsz & nlines (2048 -> 4096, 100 -> 200).
* Disabled duplicate args between parser and set_option (parser). set_option
  parser now inherits from parser, and they share a help.
* Moved logger to __main__ in order to implement multiple loggers throughout
  the package.
* DRY.
* Moved CONSTANTS to const.py to separate them, to make them editable, and
  available to __init__.py and, thus, __main__.py.
#===============================================================================
