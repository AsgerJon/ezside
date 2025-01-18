"""LayoutWindow subclasses BaseWindow and provides the widgets and layouts
of the main application window. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from PySide6.QtCore import QSize
from worktoy.desc import AttriBox, THIS, Field

from . import BaseWindow
from ..widgets import Layout, TextWidget, PushButton, PressHoldButton


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow and provides the widgets and layouts
  of the main application window. """

  grid = AttriBox[Layout](THIS)
  welcomeBanner = AttriBox[TextWidget](THIS, 'LOL!', 'MesloLGS', 40, 24)
  label = AttriBox[TextWidget](THIS, 'Button: ', 'MesloLGS', 20, 24)
  button = AttriBox[PushButton](THIS, 'CLICK ME!', )
  pressHoldButton = AttriBox[PressHoldButton](THIS, 'Hold Me!', )
  minWidth = AttriBox[int](480)
  minHeight = AttriBox[int](360)
  minSize = Field()

  @minSize.GET
  def _getMinSize(self) -> QSize:
    return QSize(self.minWidth, self.minHeight)

  if TYPE_CHECKING:
    minSize = QSize()

  def initUi(self) -> None:
    """The LayoutWindow class provides a base widget and layout."""
    self.setMinimumSize(self.minSize)
    self.grid.addWidget(self.welcomeBanner, 0, 0, 1, 2)
    self.grid.addWidget(self.label, 1, 0)
    self.grid.addWidget(self.button, 1, 1)
    self.grid.addWidget(self.pressHoldButton, 2, 0, 1, 2)
    self.setCentralWidget(self.grid.baseWidget)

  @abstractmethod
  def initLogic(self) -> None:
    """Subclasses must provide the initLogic method to provide the logic for
    the window."""
