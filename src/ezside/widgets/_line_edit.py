"""LineEdit wrapper.  """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit
from attribox import AttriBox, this
from ezside.core import Tight
from ezside.widgets import BaseWidget
from icecream import ic
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezros.rosutils import EmptyField
from ezros.widgets import Horizontal, Label


class _LineEdit(QLineEdit):
  """LineEdit wrapper.  """
  __fallback_placeholder__ = 'Enter text here'

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the widget."""
    QLineEdit.__init__(self, *args, **kwargs)


class LineEdit(BaseWidget):
  """LineEdit wrapper.  """
  __fallback_placeholder__ = 'Enter text here'
  __placeholder_text__ = None

  text = EmptyField()

  cursorPositionChanged = Signal(int, int)
  editingFinished = Signal()
  inputRejected = Signal()
  returnPressed = Signal()
  selectionChanged = Signal()
  textChanged = Signal(str)
  textEdited = Signal(str)
  baseLayout = AttriBox[Horizontal]()
  lineEdit = AttriBox[_LineEdit](this)
  placeholderText = AttriBox[str]()

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the widget."""
    BaseWidget.__init__(self, )
    placeholderKwarg = kwargs.get('placeholder', None)
    initValueKwarg = kwargs.get('initValue', None)
    strArgs = [arg for arg in args if isinstance(arg, str)]
    placeholderArg, initValueArg = [*strArgs, None, None][:2]
    initValue = maybe(initValueKwarg, initValueArg)
    if initValue is not None:
      if isinstance(initValue, str):
        self.text = initValue
      else:
        e = typeMsg('initValue', initValue, str)
        raise TypeError(e)
    self.__placeholder_text__ = maybe(placeholderKwarg,
                                      placeholderArg,
                                      self.__fallback_placeholder__)
    self.setSizePolicy(Tight, Tight)
    s = Label.getTextRect(Label(self.__placeholder_text__)).size()

    self.setMinimumSize(s)

  def initUi(self) -> None:
    """Initialize the user interface."""
    self.setSizePolicy(Tight, Tight)
    self.lineEdit.setPlaceholderText(self.__placeholder_text__)
    self.baseLayout.addWidget(self.lineEdit)
    self.setLayout(self.baseLayout)
    self.initActions()

  def initActions(self) -> None:
    """Initialize the actions."""
    self.lineEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
    self.lineEdit.editingFinished.connect(self.editingFinished)
    self.lineEdit.inputRejected.connect(self.inputRejected)
    self.lineEdit.returnPressed.connect(self.returnPressed)
    self.lineEdit.selectionChanged.connect(self.selectionChanged)
    self.lineEdit.textChanged.connect(self.textChanged)
    self.lineEdit.textEdited.connect(self.textEdited)

  def setPlaceholderText(self, text: str) -> None:
    """Set the placeholder text."""
    self.lineEdit.setPlaceholderText(text)

  @text.GET
  def __str__(self) -> str:
    """String representation"""
    return QLineEdit.text(self.lineEdit)

  @text.SET
  def setText(self, text: str) -> None:
    """Set the text."""
    QLineEdit.setText(self.lineEdit, text)
    self.update()
