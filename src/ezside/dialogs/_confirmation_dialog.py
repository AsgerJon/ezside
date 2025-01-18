"""ConfirmationDialog provides a dialog box requesting a confirmation
from the user. The box has two buttons: 'Confirm' and 'Cancel'. Hitting
the escape key is equivalent to hitting the 'Cancel' button. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias

from PySide6.QtCore import Qt, QPoint, Signal, Slot
from PySide6.QtGui import QKeyEvent, QShowEvent
from PySide6.QtWidgets import QDialog, QGridLayout, QWidget
from worktoy.desc import THIS, AttriBox

from ..core import TextModel, RGBA
from ..widgets import TextWidget, AbstractButton, PushButton, Layout

Button: TypeAlias = Qt.MouseButton


class ConfirmationDialog(QDialog):
  """ConfirmationDialog provides a dialog box requesting a confirmation
  from the user. The box has two buttons: 'Confirm' and 'Cancel'. Hitting
  the escape key is equivalent to hitting the 'Cancel' button. """

  baseLayout = AttriBox[Layout](THIS, )
  textWidget = AttriBox[TextWidget](THIS, )
  confirmButton = AttriBox[PushButton](THIS, 'Confirm')
  cancelButton = AttriBox[PushButton](THIS, 'Cancel')

  def __init__(self, *args) -> None:
    posArgs = [*args, ]
    otherArgs = []
    while posArgs:
      arg = posArgs.pop(0)
      if isinstance(arg, QWidget):
        QDialog.__init__(self, arg)
        otherArgs = [*otherArgs, *posArgs]
        break
      otherArgs.append(arg)
    else:
      QDialog.__init__(self)
    self.textWidget.label.shadowFill = RGBA(0, 0, 0, 0)
    self.textWidget.label.shadowBorder = RGBA(0, 0, 0, 0)

  def initUi(self) -> None:
    self.setWindowTitle('Confirmation')
    self.baseLayout.addWidget(self.textWidget, 0, 0, 1, 2)
    self.baseLayout.addWidget(self.cancelButton, 1, 0)
    self.baseLayout.addWidget(self.confirmButton, 1, 1)
    self.setLayout(self.baseLayout.Q)
    self.adjustSize()

  def initLogic(self) -> None:
    """Sets the logic for the dialog box."""
    self.confirmButton.pressHold.connect(self.accept)
    self.cancelButton.clicked.connect(self.reject)

  def show(self) -> None:
    """Reimplementation running initUi and initLogic before showing the
    dialog."""
    self.initUi()
    self.initLogic()
    self.setWindowModality(Qt.WindowModality.ApplicationModal)
    QDialog.show(self)

  def keyPressEvent(self, event: QKeyEvent) -> None:
    if event.keyCombination().key() == Qt.Key.Key_Escape:
      return self.reject()
    return QDialog.keyPressEvent(self, event)

  def showEvent(self, event: QShowEvent) -> None:
    """Reimplementation running initUi and initLogic before showing the
    dialog."""
    print("""Received show event: %s""" % str(event))
    self.adjustSize()
    QDialog.showEvent(self, event)
