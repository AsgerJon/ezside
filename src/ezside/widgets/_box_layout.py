"""BoxLayout provides single row or column layouts."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtWidgets import QLayout

from ezside.widgets import BaseWidget


class BoxLayout(BaseWidget):
  """BoxLayout provides single row or column layouts."""
  __base_layout__ = None

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    self.__child_widgets__ = []

  @abstractmethod
  def createBaseLayout(self) -> None:
    """Creates the base layout."""

  def getBaseLayout(self, **kwargs) -> QLayout:
    """Returns the base layout."""
    if self.__base_layout__ is None:
      if kwargs.get('_recursion', None):
        raise RecursionError
      self.createBaseLayout()
      return self.getBaseLayout(_recursion=True)
    return self.__base_layout__

  def setBaseLayout(self, layout: QLayout) -> None:
    """Sets the base layout."""
    self.__base_layout__ = layout

  def addWidget(self, *args) -> None:
    """Adds a widget to the layout. """
    for arg in args:
      if isinstance(arg, BaseWidget):
        widget = arg
        break
    else:
      raise ValueError('Received no widget!')
    self.__child_widgets__.append(widget)
    widget.initUi()
    widget.connectActions()
    self.getBaseLayout().addWidget(widget)

  def reset(self) -> None:
    """Rebuilds the layout."""
    setattr(self, '__base_layout__', None)
    self.createBaseLayout()
    for widget in self.__child_widgets__:
      self.addWidget(widget)
    self.setLayout(self.getBaseLayout())
