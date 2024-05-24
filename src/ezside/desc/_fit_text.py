"""The 'fitText' function fits text into lines of a given width. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


def fitText(text: str, width: int, ) -> list[list[str]]:
  """Fits text into lines of a given width. """
  lines = []
  line = []
  for word in text.split():
    if sum([len(word) for word in line]) + len(line) - 1 > width - len(word):
      lines.append(line)
      line = []
    line.append(word)
  return lines
