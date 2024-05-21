"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF
from PySide6.QtGui import QFont
from attribox import AttriBox
from icecream import ic
from vistutils.fields import EmptyField
from vistutils.parse import maybe

from ezside.core import parseLineLength
from ezside.widgets import CanvasWidget
from moreattribox import Flag

ic.configureOutput(includeContext=True, )


class Label(CanvasWidget):
  """Label provides the general class for widgets"""

  __fallback_text__ = 'LMAO'

  text = AttriBox[str]()
  lineCharLength = AttriBox[int]()
  justify = Flag(True)
  fontMetrics = EmptyField()
  font = AttriBox[QFont]()

  def __init__(self, *args, **kwargs) -> None:
    CanvasWidget.__init__(self, *args, **kwargs)
    for arg in args:
      if isinstance(arg, str):
        self.text = arg
        break
    else:
      self.text = self.__fallback_text__
    self.lineCharLength = maybe(parseLineLength(*args, **kwargs), 0)

  def fitText(self, *args) -> QRectF:
    """Fit the text. If self.lineCharLength is set, the text will be split
    in lines consisting of full words such that each line has at most
    self.lineCharLength characters. Please note that this does not take
    into account the current font. """

  def initUi(self, ) -> None:
    """Initialize the user interface."""

  def initSignalSlot(self) -> None:
    """Initialize the signal slot."""
