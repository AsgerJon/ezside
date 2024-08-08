"""NewDialog opens a dialog asking for a file name and for the dimensions
of the new image. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QDialog, QSpinBox, QVBoxLayout, QLineEdit, \
  QHBoxLayout, QWidget
from worktoy.desc import THIS, AttriBox, Field

from ezside.dialogs import SaveFileDialog
from ezside.tools import SizeRule
from ezside.basewidgets import Label, BoxWidget, PushButton


class NewDialog(QDialog):
  """NewDialog opens a dialog asking for a file name and for the dimensions
  of the new image. """

  __fallback_width__ = 256
  __fallback_height__ = 256
  __fallback_file_name__ = 'unnamed.png'

  width = Field()
  height = Field()
  fileName = Field()

  @width.GET
  def _getWidth(self) -> int:
    """Getter-function for the width attribute"""
    return self.widthSpinBox.value()

  @height.GET
  def _getHeight(self) -> int:
    """Getter-function for the height attribute"""
    return self.heightSpinBox.value()

  @fileName.GET
  def _getFileName(self) -> str:
    """Getter-function for the file name attribute"""
    return self.fileNameLineEdit.text()

  baseLayout = AttriBox[QVBoxLayout]()

  widthLayout = AttriBox[QHBoxLayout]()
  widthWidget = AttriBox[BoxWidget](THIS)
  widthLabel = AttriBox[Label](THIS, 'Width')
  widthSpinBox = AttriBox[QSpinBox](THIS)

  heightLayout = AttriBox[QHBoxLayout]()
  heightWidget = AttriBox[BoxWidget](THIS)
  heightLabel = AttriBox[Label](THIS, 'Height')
  heightSpinBox = AttriBox[QSpinBox](THIS)

  fileNameLayout = AttriBox[QHBoxLayout]()
  fileNameWidget = AttriBox[BoxWidget](THIS)
  fileNameLabel = AttriBox[Label](THIS, 'File Name')
  fileNameLineEdit = AttriBox[QLineEdit](THIS)
  fileButton = AttriBox[PushButton](THIS, '...')

  buttonLayout = AttriBox[QHBoxLayout]()
  buttonWidget = AttriBox[BoxWidget](THIS)
  cancelButton = AttriBox[PushButton](THIS, 'Cancel')
  acceptButton = AttriBox[PushButton](THIS, 'Accept')

  spacer = AttriBox[BoxWidget](THIS)

  saveFileDialog = AttriBox[SaveFileDialog]()

  def initUi(self) -> None:
    """Sets the layout of the dialog"""
    self.widthLabel.text = 'Width: '
    self.widthLabel.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.widthWidget.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.widthSpinBox.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.widthSpinBox.setMinimum(32)
    self.widthSpinBox.setMaximum(4096)
    self.widthSpinBox.setValue(self.__fallback_width__)
    self.widthLayout.addWidget(self.widthLabel)
    self.widthLayout.addWidget(self.widthSpinBox)
    self.widthWidget.setLayout(self.widthLayout)

    self.heightLabel.text = 'Height: '
    self.heightLabel.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.heightWidget.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.heightSpinBox.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.heightSpinBox.setMinimum(32)
    self.heightSpinBox.setMaximum(4096)
    self.heightSpinBox.setValue(self.__fallback_height__)
    self.heightLayout.addWidget(self.heightLabel)
    self.heightLayout.addWidget(self.heightSpinBox)
    self.heightWidget.setLayout(self.heightLayout)

    self.fileNameLabel.text = 'File Name: '
    self.fileNameLabel.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.fileNameWidget.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.fileNameLineEdit.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.fileButton.sizeRule = SizeRule.EXPAND + SizeRule.CONTRACT
    self.fileNameLineEdit.setText(self.__fallback_file_name__)
    self.fileNameLayout.addWidget(self.fileNameLabel)
    self.fileNameLayout.addWidget(self.fileNameLineEdit)
    self.fileNameLayout.addWidget(self.fileButton)
    self.fileNameWidget.setLayout(self.fileNameLayout)

    self.buttonLayout.addWidget(self.cancelButton)
    self.buttonLayout.addWidget(self.acceptButton)
    self.buttonWidget.setLayout(self.buttonLayout)

    self.spacer.backgroundColor = QColor(191, 191, 191, 255)
    self.spacer.sizeRule = SizeRule.EXPAND
    self.spacer.setMinimumSize(400, 16)
    self.baseLayout.addWidget(self.widthWidget)
    self.baseLayout.addWidget(self.heightWidget)
    self.baseLayout.addWidget(self.fileNameWidget)
    self.baseLayout.addWidget(self.buttonWidget)

    self.baseLayout.addWidget(self.spacer)
    self.setLayout(self.baseLayout)

  def initSignalSlot(self) -> None:
    """Connects the signals and slots"""
    self.fileButton.leftClick.connect(self.saveFileDialog.show)
    self.saveFileDialog.fileSelected.connect(
        self.fileNameLineEdit.setText)
    self.cancelButton.leftClick.connect(self.close)
    self.acceptButton.leftClick.connect(self.accept)

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QDialog.__init__(self, arg)
        break
    else:
      QDialog.__init__(self)

  def show(self) -> None:
    """Reimplementation"""
    self.initUi()
    self.initSignalSlot()
    QDialog.show(self)
