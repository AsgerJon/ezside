"""TextBox provides a flexible text display implementing word wrapping and
text alignment. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from attribox import AttriBox
from vistutils.parse import maybe

from ezside.core import Alignment, \
  AlignLeft, \
  AlignTop, \
  parseLineLength, \
  parseText, parseAlignment
from ezside.widgets import CanvasWidget


class TextBox(CanvasWidget):
  """TextBox provides a flexible text display implementing word wrapping and
  text alignment. """

  __fallback_line_length__ = 77
  __fallback_text__ = 'LMAO'
  __horizontal_alignment__ = None
  __vertical_alignment__ = None
  __fallback_horizontal_alignment__ = AlignLeft
  __fallback_vertical_alignment__ = AlignTop

  lineLength = AttriBox[int]()
  text = AttriBox[str]()
  alignment = Alignment()

  def __init__(self, *args, **kwargs) -> None:
    CanvasWidget.__init__(self, *args, **kwargs)
    lineLength = parseLineLength(*args, **kwargs)
    self.lineLength = maybe(lineLength, self.__fallback_line_length__)
    text = parseText(*args, **kwargs)
    self.text = maybe(text, self.__fallback_text__)
    alignment = parseAlignment(*args, **kwargs)
    self.alignment = maybe(alignment, self.__fallback_horizontal_alignment__)
