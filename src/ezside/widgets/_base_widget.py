"""
BaseWidget provides a base class for the widgets. Using AttriBox they
provide brushes, pens and fonts as attributes. These widgets are not meant
for composite widgets directly but instead for the constituents. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget
from attribox import AttriBox
from ezside.settings import Defaults

from ezside.moreutils import EmptyField
from icecream import ic

from ezside.core import parseParent, NoWrap, Center, Pen, Font, Brush
from ezside.core import BevelJoin, FlatCap, SolidLine, SolidFill, DashLine
from ezside.core import DotLine, DashDot

ic.configureOutput(includeContext=True, )


class BaseWidget(QWidget):
  """BaseWidget provides a base class for the widgets. Using AttriBox they
  provide brushes, pens and fonts as attributes. These widgets are not meant
  for composite widgets directly but instead for the constituents. """

  defaults = AttriBox[Defaults](os.environ.get('SETTINGS_FILE', None))
  baseSize = AttriBox[QSize](32, 32)

  def __init__(self, *args, **kwargs) -> None:
    """BaseWidget provides a base class for the widgets. Using AttriBox they
    provide brushes, pens and fonts as attributes. These widgets are not
    meant for composite widgets directly but instead for the components."""
    # ic('%s' % self.__class__.__name__)
    parent = parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    self.setMinimumSize(QSize(64, 64))
    # self.initUi()

  def initUi(self) -> None:
    """The initUi method initializes the user interface of the window."""
    self.setMinimumSize(self.baseSize)
    self.connectActions()

  def connectActions(self) -> None:
    """The connectActions method connects the actions to the signals."""
