"""The findBetween function finds text between two delimiters. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic

ic.configureOutput(includeContext=True)


def _findIn(text: str, searchTerm: str, charIndex: int = None) -> list[int]:
  """Returns the indexes of the first or last letter in searchTerm for each
  occurrence in the text determined by the charIndex. This may be 0 to
  indicate first, -1 to indicate last, an integer in range. Default is 0."""
  out = []
  charIndex = 0 if charIndex is None else charIndex
  n = len(searchTerm)
  for (i, char) in enumerate(text):
    if text[i:i + n] == searchTerm:
      out.append(i + (charIndex % n))
  return out


def _monoIndices(text: str, mono: str, *args) -> Any:
  """Updates the text so that every other occurrence of the mono is
  replaced by 'first' or 'last'. """
  n, a, b = len(mono), None, None
  for arg in args:
    if isinstance(arg, str):
      if a is None:
        a = arg
      elif b is None:
        b = arg
      else:
        break
  else:
    a = '{{START}}' if a is None else a
    b = '{{END}}' if b is None else b
  print(a, b)
  startInd = [*_findIn(text, mono, -1)]
  lastInd = [0, *_findIn(text, mono, ), len(text)]
  running = 0
  newText = ''
  for (i, (start, last)) in enumerate(zip(startInd, lastInd)):
    newWord = (b if i % 2 else a)
    wordLen = len(newWord)
    firstBit = text[last + 1:start]
    entry = '%s%s' % (firstBit, newWord,)
    newText += entry
    running += len(firstBit + mono)
  return newText


def findBetween(text: str, first: str, last: str) -> list[str]:
  """Finds the text between the start and end delimiters. """
  if first == last:
    mono = first
    ic(mono)
    firstLim = '<%s>' % mono
    lastLim = '</%s>' % mono
    text = _monoIndices(text, mono, firstLim, lastLim)
    return findBetween(text, firstLim, lastLim)
  out = []
  if first == last:
    firstInd = _findIn(text, first, 0, )[1:]
    lastInd = _findIn(text, last, -1)[:-1]
    for (i, (first, last)) in enumerate(zip(firstInd, lastInd)):
      if (i + 1) % 2:
        out.append(text[first:last])
    return out
  firstInd = _findIn(text, first, -1)
  lastInd = _findIn(text, last, 0)
  for (first, last) in zip(firstInd, lastInd):
    out.append(text[first + 1:last])
  return out
