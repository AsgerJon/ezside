"""Chapter provides the top level abstraction in the typographinator
abstraction. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING, Self

from moreattribox.typographinator import Paragraph

if TYPE_CHECKING:
  pass


class Chapter:
  """Chapter provides the top level abstraction in the typographinator
  abstraction. """

  __inner_paragraphs__ = None
  __iter_contents__ = None

  def __iter__(self) -> Self:
    self.__iter_contents__ = [*self.__inner_paragraphs__, ]
    return self

  def __next__(self, ) -> Paragraph:
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def append(self, paragraph: Paragraph) -> None:
    """Appends a paragraph to the chapter."""
    self.__inner_paragraphs__.append(paragraph)

  def __len__(self, ) -> int:
    return len(self.__inner_paragraphs__)

  def __getitem__(self, index: int) -> Paragraph:
    if index > len(self):
      raise IndexError
    if index < 0:
      return self[len(self) + index]
    return self.__inner_paragraphs__[index]

  def __setitem__(self, index: int, paragraph: Paragraph) -> None:
    self.__inner_paragraphs__[index] = paragraph

  def __str__(self, ) -> str:
    return '\n'.join(self.getLines())

  def __abs__(self, ) -> int:
    return len(str(self).split('\n'))

  def getLines(self) -> list[str]:
    """Returns the lines of the chapter."""
    out = []
    for (i, paragraph) in enumerate(self):
      for line in paragraph.getLines():
        out.append(line)
      else:
        for item in ['', '', paragraph.getHeader('-%02d-' % i), '', '']:
          out.append(item)
    return out
