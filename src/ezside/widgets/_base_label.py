"""BaseLabel provides a simple label"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel
from attribox import AttriBox
from vistutils.waitaminute import typeMsg

from ezside.widgets import BaseWidget, Grid


class BaseLabel(BaseWidget):
  """BaseLabel provides a simple label"""

  __inner_label__ = None

  innerText = AttriBox[str]('lmao')
  baseLayout = AttriBox[Grid]()

  def __init__(self, innerText: str = 'lmao') -> None:
    """Initialize the BaseLabel."""
    self.innerText = innerText
    BaseWidget.__init__(self)

  def _createLabel(self) -> None:
    """Create the label."""
    if self.__inner_label__ is not None:
      e = """The label has already been created."""
      raise AttributeError(e)
    self.__inner_label__ = QLabel()
    self.__inner_label__.setText(self.innerText)
    font = QFont()
    font.setFamily('Montserrat')
    font.setPointSize(12)
    self.__inner_label__.setFont(font)
    self.__inner_label__.setText(self.innerText)

  def _getLabel(self, **kwargs) -> QLabel:
    """Return the label."""
    if self.__inner_label__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createLabel()
      return self._getLabel(_recursion=True)
    if isinstance(self.__inner_label__, QLabel):
      return self.__inner_label__
    e = typeMsg('innerLabel', self.__inner_label__, QLabel)
    raise TypeError(e)

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.baseLayout.addWidget(self._getLabel())
    self.setLayout(self.baseLayout)

  @innerText.ONSET
  def _newText(self, oldText: str, newText: str) -> None:
    """Notified when value of innerText changes. """
    if oldText != newText:
      self._getLabel().setText(newText)
      self._getLabel().update()
 