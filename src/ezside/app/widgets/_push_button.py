"""PushButton subclasses AbstractButton and implements a stateless,
hover-aware push button. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from PySide6.QtCore import Signal, Slot, QPoint, Qt, QSize
from PySide6.QtGui import QPainter
from worktoy.text import typeMsg
from worktoy.parse import maybe
from worktoy.desc import Field

from . import AbstractButton, PushButtonConfig
from ..core import RGBA, BoxModel, TextModel, Rect, Font
from ..enums import MouseButton, Align

PaintJob: TypeAlias = tuple[Rect, QPainter]


class _FieldValue:
  """Data descriptor. """


class _ConfigValues:
  """Class providing static configuration values."""

  baseWidth = 1
  hoverWidth = 2
  pressedWidth = 3
  baseCorner = 4
  hoverCorner = 9
  pressedCorner = 16

  enabledFill = RGBA(191, 191, 191, 255)
  enabledBorder = RGBA(0, 0, 0, 255)
  disabledFill = RGBA(223, 223, 223, 255)
  disabledBorder = RGBA(191, 191, 191, 255)


class PushButton(AbstractButton):
  """PushButton subclasses AbstractButton and implements a stateless,
  hover-aware push button. """

  __text_model__ = None

  label = Field()

  __enabled_fallback__ = True
  __enabled_flag__ = None

  disabledBaseBox = PushButtonConfig(
      _ConfigValues.disabledFill,
      _ConfigValues.disabledBorder,
      _ConfigValues.baseWidth,
      _ConfigValues.baseCorner,
  )
  disabledHoverBox = PushButtonConfig(
      _ConfigValues.disabledFill,
      _ConfigValues.disabledBorder,
      _ConfigValues.hoverWidth,
      _ConfigValues.hoverCorner,
  )

  disabledPressedBox = PushButtonConfig(
      _ConfigValues.disabledFill,
      _ConfigValues.disabledBorder,
      _ConfigValues.pressedWidth,
      _ConfigValues.pressedCorner,
  )

  enabledBaseBox = PushButtonConfig(
      _ConfigValues.enabledFill,
      _ConfigValues.enabledBorder,
      _ConfigValues.baseWidth,
      _ConfigValues.baseCorner,
  )

  enabledHoverBox = PushButtonConfig(
      _ConfigValues.enabledFill,
      _ConfigValues.enabledBorder,
      _ConfigValues.hoverWidth,
      _ConfigValues.hoverCorner,
  )

  enabledPressedBox = PushButtonConfig(
      _ConfigValues.enabledFill,
      _ConfigValues.enabledBorder,
      _ConfigValues.pressedWidth,
      _ConfigValues.pressedCorner,
  )

  isEnabled = Field()

  nowEnabled = Signal()
  nowDisabled = Signal()
  alreadyEnabled = Signal()
  alreadyDisabled = Signal()
  disabledClick = Signal()  # Triggered by any button when disabled
  clicked = Signal()  # Triggered by left-click
  contextMenu = Signal()  # Triggered by right-click
  disabledPressHold = Signal()  # Triggered by long press of any button
  pressHold = Signal()  # Triggered by long press of any button

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
  def _setLabel(self, newText: str, **kwargs) -> None:
    """The setter function changes the text in the label attribute to the
    given value. """
    if self.__text_model__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createLabel()
      return self._setLabel(newText, _recursion=True)
    if isinstance(newText, str):
      self.__text_model__.text = newText
      return
    if isinstance(newText, TextModel):
      if kwargs.get('_recursion2', False):
        raise RecursionError
      return self._setLabel(newText.text, _recursion2=True)
    if isinstance(newText, bytes):
      if kwargs.get('_recursion3', False):
        raise RecursionError
      return self._setLabel(newText.decode(), _recursion3=True)
    e = typeMsg('newText', newText, str)
    raise TypeError(e)

  def __bool__(self, ) -> bool:
    """Returns the state of the button. """
    return True if self._getEnabled() else False

  @isEnabled.GET
  def _getEnabled(self) -> bool:
    """Returns the state of the button. """
    return maybe(self.__enabled_flag__, self.__enabled_fallback__)

  @isEnabled.SET
  def _setEnabled(self, value: bool) -> None:
    """Sets enabled flag of the button. """
    newFlag = True if value else False
    oldFlag = self._getEnabled()
    if newFlag != oldFlag:
      self.__enabled_flag__ = newFlag
      if newFlag:
        self.nowEnabled.emit()
      else:
        self.nowDisabled.emit()
    else:
      if newFlag:
        self.alreadyEnabled.emit()
      else:
        self.alreadyDisabled.emit()

  @Slot(bool)
  def setEnabled(self, value: bool) -> None:
    """Alias for _setState. """
    return self._setEnabled(value)

  @Slot()
  def enable(self, ) -> None:
    """Enables the button. """
    self._setEnabled(True)

  @Slot()
  def disable(self, ) -> None:
    """Disables the button. """
    self._setEnabled(False)

  @Slot()
  def toggle(self, ) -> None:
    """Toggles the button state. """
    self._setEnabled(False if self._getEnabled() else True)

  def getBoxModel(self, **kwargs) -> BoxModel:
    """Returns a box model for this widget appropriate for the current
    state. """
    if self._getEnabled():
      if self.isPressed:
        return self.enabledPressedBox
      elif self.underMouse:
        return self.enabledHoverBox
      return self.enabledBaseBox
    if self.isPressed:
      return self.disabledPressedBox
    elif self.underMouse:
      return self.disabledHoverBox
    return self.disabledBaseBox

  def initUi(self, ) -> None:
    AbstractButton.initUi(self)
    self.singleClick.connect(self._clickedFunc)
    self.doubleClick.connect(self._clickedFunc)
    self.tripleClick.connect(self._clickedFunc)
    self.singlePressHold.connect(self._pressHoldFunc)
    self.doublePressHold.connect(self._pressHoldFunc)
    self.triplePressHold.connect(self._pressHoldFunc)
    self.nowEnabled.connect(self.update)
    self.nowDisabled.connect(self.update)
    self.alreadyEnabled.connect(self.update)
    self.alreadyDisabled.connect(self.update)

  @Slot(Qt.MouseButton, QPoint)
  def _clickedFunc(self, btn: Qt.MouseButton, pnt: QPoint) -> None:
    """Wrapper on the clicked signal. """
    if not self:
      return self.disabledClick.emit()
    button = MouseButton.fromQ(btn)
    if button is MouseButton.LEFT:
      self.clicked.emit()
    elif button is MouseButton.RIGHT:
      self.contextMenu.emit()

  @Slot(Qt.MouseButton, QPoint)
  def _pressHoldFunc(self, btn: Qt.MouseButton, pnt: QPoint) -> None:
    """Wrapper on the pressHold signal. """
    self.pressHold.emit() if self else self.disabledPressHold.emit()

  def paintContent(self, rect: Rect, painter: QPainter) -> PaintJob:
    """Paints the content of the widget. """
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    rect, painter = AbstractButton.paintContent(self, rect, painter)
    painter = self.label.paint(painter, rect)
    return rect, painter

  def __init__(self, *args) -> None:
    """Initializes the ButtonWidget. """
    AbstractButton.__init__(self, *args)
    parent = self.parent()
    otherArgs = [arg for arg in args if arg is not parent]
    self.label = TextModel(*otherArgs)
    self.setMouseTracking(True)
    self.label.align = Align.CENTER
    self.label.font = Font('MesloLGS NF', 18)
    self.label.lineLength = 40
    self.label.fontColor = RGBA(0, 0, 0, 255)
    self.label.shadowFill = RGBA(0, 0, 0, 0, )
    self.label.shadowBorder = RGBA(0, 0, 0, 0, )

  def minimumSize(self) -> QSize:
    """Getter-function for the minimumSize attribute. """
    if TYPE_CHECKING:
      assert isinstance(self.label, TextModel)
    return self.getBoxModel().fitSize(self.label.shadowSize).Q

  def minimumSizeHint(self) -> QSize:
    """Getter-function for the minimumSizeHint attribute. """
    return self.minimumSize()
