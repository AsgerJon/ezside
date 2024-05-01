"""The 'layouts' provide for initialization of the widget at the moment
addWidget is invoked."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget
from icecream import ic

from ezside.core import Tight, AlignTop, AlignLeft
from ezside.widgets import BaseWidget

from ezside.settings import Defaults

ic.configureOutput(includeContext=True, )


class Grid(QGridLayout):
  """GridLayout class provides a grid layout for the application."""

  def __init__(self, *args, **kwargs) -> None:
    QGridLayout.__init__(self, *args, **kwargs)
    margins = Defaults.getLayoutMargins()
    spacing = Defaults.getLayoutSpacing()
    self.setContentsMargins(Defaults.getLayoutMargins())
    self.setSpacing(Defaults.getLayoutSpacing())

  def addWidget(self, widget: QWidget, *args, **kwargs) -> None:
    """Add a widget to the layout."""
    if isinstance(widget, BaseWidget):
      BaseWidget.generalInit(widget)
      widget.initUi()
      widget.connectActions()
    QGridLayout.addWidget(self, widget, *args, **kwargs)


class Vertical(QVBoxLayout):
  """VBoxLayout class provides a vertical layout for the application."""

  def __init__(self, *args, **kwargs) -> None:
    QVBoxLayout.__init__(self, *args, **kwargs)
    margins = Defaults.getLayoutMargins()
    spacing = Defaults.getLayoutSpacing()
    self.setContentsMargins(Defaults.getLayoutMargins())
    self.setSpacing(Defaults.getLayoutSpacing())

  def addWidget(self, widget: QWidget, *args, **kwargs) -> None:
    """Add a widget to the layout."""
    if isinstance(widget, BaseWidget):
      BaseWidget.generalInit(widget)
      widget.initUi()
      widget.connectActions()
    QVBoxLayout.addWidget(self, widget, **kwargs)


class Horizontal(QHBoxLayout):
  """HBoxLayout class provides a horizontal layout for the application."""

  def __init__(self, *args, **kwargs) -> None:
    QHBoxLayout.__init__(self, *args, **kwargs)
    margins = Defaults.getLayoutMargins()
    spacing = Defaults.getLayoutSpacing()
    self.setContentsMargins(Defaults.getLayoutMargins())
    self.setSpacing(Defaults.getLayoutSpacing())

  def addWidget(self, widget: QWidget, *args, **kwargs) -> None:
    """Add a widget to the layout."""
    if isinstance(widget, BaseWidget):
      BaseWidget.generalInit(widget)
      widget.initUi()
      widget.connectActions()
    QVBoxLayout.addWidget(self, widget, **kwargs)
