"""The 'textWrap' function receives an integer describing the line length
in characters and any number of strings arguments. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any, Callable

from vistutils.waitaminute import typeMsg


def _charCount(*words: str) -> int:
  """Counts the number of characters in the words including spaces."""
  if not words:
    return 0
  if len(words) == 1:
    return len(words[0].strip())
  out = 0
  for word in words:
    if word:
      out += len(word.strip())
  return out + len(words) - 1


def _typeGuard(arg: Any) -> Never:
  """Raises a TypeError."""
  if isinstance(arg, str):
    return arg
  e = typeMsg('word', arg, str)
  raise TypeError(e)


def _laxConvert(arg: Any) -> str:
  """Converts the argument to a string."""
  if isinstance(arg, str):
    return arg
  if '__str__' in arg.__class__.__dict__:
    return arg.__class__.__str__(arg)
  return object.__str__(arg)


def _getWords(*args, **kwargs) -> list[str]:
  """The '_getWords' function receives any number of arguments and returns a
  list of words. Use keyword argument 'strict' to specify that only
  arguments of type 'str' are allowed. Use 'convert' to specify how
  instances of types other than 'str' should be handled. Provide a bool or
  a callable. If True (default) non 'str' instances are converted using:
  arg.__class__.__str__. If False, non 'str' instances are ignored. If a
  callable, the return value of the callable is added tot the list.

  Please note that the 'strict' and 'convert' arguments are mutually
  exclusive. """
  strict = True if kwargs.get('strict', False) else False
  convert = kwargs.get('convert', None)

  if strict and convert is not None:
    e = """The 'strict' and 'convert' arguments are mutually exclusive."""
    raise ValueError(e)
  if convert is None and strict:
    convert = _typeGuard
  elif convert is None:  # Default
    convert = _laxConvert
  elif not callable(convert):
    e = typeMsg('convert', convert, Callable)
    raise TypeError(e)
  words = []
  for arg in args:
    for word in arg.split():
      words.append(word)
  return words


def textWrap(*args) -> list[str]:
  """The 'textWrap' function receives an integer describing the line length
  in characters and any number of strings arguments. """
  if not args:
    return []
  lineChars, words = None, None
  for (i, arg) in enumerate(args):
    if isinstance(arg, int):
      break
  else:
    e = """No line length was provided!"""
    raise ValueError(e)
  words = [*args, ]
  lineChars = words.pop(i)
  if not words:
    return []
  words = _getWords(*words)
  lines = []
  line = []
  while words:
    word = words.pop(0)
    if _charCount(*line, word) <= lineChars:
      line.append(word)
    elif words:
      lines.append(' '.join(line))
      line = [word, ]
    else:
      break
  else:
    lines.append(' '.join(line))
  return lines
