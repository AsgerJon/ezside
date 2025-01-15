"""TextWidget provides a widget displaying text as defined by alignment
and font. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

from PySide6.QtCore import Slot, QSize, Signal
from PySide6.QtGui import QPainter, QShowEvent
from PySide6.QtWidgets import QWidget, QSizePolicy
from worktoy.desc import AttriBox, Field
from worktoy.text import typeMsg

from . import AbstractWidget
from ..core import Rect, TextModel

PaintJob: TypeAlias = tuple[Rect, QPainter]


class TextWidget(AbstractWidget):
  """TextWidget provides a widget displaying text as defined by alignment
  and font. """

  __text_model__ = None

  sizeUpdate = Signal()
  label = Field()

  def _createLabel(self, *args, **kwargs) -> None:
    """Creator function for the label attribute. """
    self.__text_model__ = TextModel(*args, **kwargs)

  @label.GET
  def _getLabel(self, **kwargs) -> TextModel:
    """Getter-function for the label attribute. """
    if self.__text_model__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createLabel()
      return self._getLabel(_recursion=True)
    if isinstance(self.__text_model__, TextModel):
      return self.__text_model__
    e = typeMsg('__text_model__', self.__text_model__, TextModel)
    raise TypeError(e)

  @label.SET
  def _setLabel(self, newText: str, ) -> None:
    """The setter function changes the text in the label attribute to the
    given value. """
    if not isinstance(newText, str):
      e = typeMsg('newText', newText, str)
      raise TypeError(e)
    self.__text_model__.text = newText

  def paintContent(self, rect: Rect, painter: QPainter) -> PaintJob:
    """Implementation of the paintContent method. """
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    return rect, self.label.paint(painter, rect)

  def __init__(self, *args, **kwargs) -> None:
    """Constructor for the TextWidget class. """
    for arg in [*args, ]:
      if isinstance(arg, QWidget):
        AbstractWidget.__init__(self, arg)
        self._createLabel(*[a for a in args if a is not arg])
        break
    else:
      AbstractWidget.__init__(self)
      self._createLabel(*args)

  def initUi(self, ) -> None:
    """Implementation of the initUi method. """
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    maxPolicy = QSizePolicy.Policy.Maximum
    prefPolicy = QSizePolicy.Policy.Preferred
    self.setSizePolicy(prefPolicy, maxPolicy)
    self.setText(self.label.text)
    self.adjustSize()

  @Slot(str)
  def setText(self, text: str) -> None:
    """Slot for setting the text of the widget. """
    self.label.text = text
    self.updateGeometry()

  def getText(self) -> str:
    """Getter-function for the text attribute. """
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    return self.label.text

  def minimumSize(self) -> QSize:
    """Getter-function for the minimumSize attribute. """
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    return self.getBoxModel().fitSize(self.label.shadowSize).Q

  def minimumSizeHint(self) -> QSize:
    """Getter-function for the minimumSizeHint attribute. """
    return self.minimumSize()

  def showEvent(self, show: QShowEvent) -> None:
    """Overrides the QWidget showEvent function. """
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    _text = self.label.text
    self.setText(_text)
    QWidget.showEvent(self, show)
