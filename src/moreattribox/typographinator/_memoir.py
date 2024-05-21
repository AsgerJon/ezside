"""Memoir provides the top level abstraction in the typographinator. This
class provides the functionality used in the typographinator to render
text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from attribox import AttriBox
from vistutils.parse import maybe

from moreattribox.typographinator import Chapter


class Memoir:
  """Memoir provides the top level abstraction in the typographinator. This
  class provides the functionality used in the typographinator to render
  text. """

  __page_length__ = None
  __fallback_page_length__ = 24
  __inner_chapters__ = None
  __iter_contents__ = None

  lineLength = AttriBox[int]()

  def __iter__(self) -> Self:
    self.__iter_contents__ = [*self.__inner_chapters__, ]
    return self

  def __next__(self, ) -> Chapter:
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __getitem__(self, index: int) -> Chapter:
    if index > len(self):
      raise IndexError
    if index < 0:
      return self[len(self) + index]
    return self.__inner_chapters__[index]

  def __len__(self, ) -> int:
    return len(self.__inner_chapters__)

  def __int__(self, ) -> int:
    return maybe(self.__page_length__, self.__fallback_page_length__)

  def getLines(self) -> list[str]:
    """Returns the lines of the memoir."""
    out = []
    for chapter in self:
      for line in chapter.getLines():
        out.append(line)
      else:
        while len(out) % int(self):
          out.append('')
    return out
