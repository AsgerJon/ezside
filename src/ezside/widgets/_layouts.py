"""The 'layouts' provide for initialization of the widget at the moment
addWidget is invoked."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from ezside.widgets import BaseWidget


def addInit(cls: type) -> type:
  """Apply the extension to the class."""

  oldAddWidget = getattr(cls, 'addWidget', )
  oldInit = getattr(cls, '__init__', )

  def addWidget(this: cls, *args) -> None:
    """Add a widget to the layout."""
    for arg in args:
      if isinstance(arg, BaseWidget):
        arg.initUi()
        arg.connectActions()
        break
    return oldAddWidget(this, *args)

  def newInit(this: cls, *args, **kwargs) -> None:
    """Initialize the class."""
    oldInit(this, *args, **kwargs)
    this.setSpacing(2)
    this.setContentsMargins(2, 2, 2, 2, )

  setattr(cls, 'addWidget', addWidget)
  setattr(cls, '__init__', newInit)
  return cls


@addInit
class Grid(QGridLayout):
  """GridLayout class provides a grid layout for the application."""

  def __init__(self, *args, **kwargs) -> None:
    QGridLayout.__init__(self, *args, **kwargs)


@addInit
class Vertical(QVBoxLayout):
  """VBoxLayout class provides a vertical layout for the application."""

  def __init__(self, *args, **kwargs) -> None:
    QVBoxLayout.__init__(self, *args, **kwargs)


@addInit
class Horizontal(QHBoxLayout):
  """HBoxLayout class provides a horizontal layout for the application."""

  def __init__(self, *args, **kwargs) -> None:
    QHBoxLayout.__init__(self, *args, **kwargs)
