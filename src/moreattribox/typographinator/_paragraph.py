"""Paragraph provides the next level of abstraction in the typographinator
abstraction. Instances of paragraph are iterable, indexable and mutable
with each element being an instance of Word. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from moreattribox.typographinator import Word


class Paragraph:
  """Paragraph provides the next level of abstraction in the typographinator
  abstraction. Instances of paragraph are iterable, indexable and mutable
  with each element being an instance of Word. """

  __fallback_length__ = 77
  __inner_words__ = None
  __iter_contents__ = None
  __paragraph_header__ = None

  @staticmethod
  def _parseStr(*args) -> list[Word]:
    """Parses the input string into a list of words."""
    out = []
    for arg in args:
      if isinstance(arg, str):
        for word in arg.split():
          out.append(Word(word))
    return out

  def __len__(self, ) -> int:
    return len(self.__inner_words__)

  def __init__(self, *args, **kwargs) -> None:
    self.__inner_words__ = self._parseStr(*args)

  def __iter__(self) -> Self:
    self.__iter_contents__ = [*self.__inner_words__, ]
    return self

  def __next__(self, ) -> Word:
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __getitem__(self, index: int) -> Word:
    if index > len(self):
      raise IndexError
    if index < 0:
      return self[len(self) + index]
    return self.__inner_words__[index]

  def __setitem__(self, index: int, word: Word) -> None:
    self.__inner_words__[index] = word

  def getHeader(self, fallback: str = None) -> str:
    """Returns the header of the paragraph."""
    header = maybe(self.__paragraph_header__, fallback)
    if header is None:
      e = """Instance of '%s' has no defined header, and no fallback 
      header was provided!"""
      raise ValueError(monoSpace(e % self.__class__.__name__))
    if isinstance(header, str):
      return header
    e = typeMsg('header', header, str)
    raise TypeError(monoSpace(e))

  def __str__(self, ) -> str:
    """Renders the paragraph."""
    lineLength = self.__fallback_length__
    lines = []
    line = []
    for word in self:
      if len(line) + len(word) > lineLength:
        lines.append(' '.join([str(w) for w in line]))
        line = []
      line.append(word if line else +word)
    else:
      if line:
        lines.append(' '.join([str(w) for w in line]))
    return '\n'.join(lines)

  def getLines(self, lineLength: int = None) -> list[str]:
    """Returns the lines of the paragraph."""
    lines = []
    line = []
    for word in self:
      if len(line) + len(word) > lineLength:
        lines.append(' '.join([str(w) for w in line]))
        line = []
      line.append(word if line else +word)
    else:
      if line:
        lines.append(' '.join([str(w) for w in line]))
    return lines
