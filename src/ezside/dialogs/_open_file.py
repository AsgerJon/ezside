"""OpenFile dialog provides a dialog for selecting an existing file. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSettings, QByteArray
from PySide6.QtGui import QCloseEvent, QMouseEvent
from PySide6.QtWidgets import QFileDialog
from icecream import ic

ic.configureOutput(includeContext=True)


class OpenFileDialog(QFileDialog):
  """OpenFile dialog provides a dialog for selecting an existing file. """

  def __init__(self, parent=None) -> None:
    QFileDialog.__init__(self, parent)
    self.setMouseTracking(True)
    state = QSettings().value('OpenFileDialog/saveState', None)
    if isinstance(state, QByteArray):
      self.restoreState(state)
    self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    self.setFileMode(QFileDialog.FileMode.ExistingFile)
    self.setViewMode(QFileDialog.ViewMode.Detail)
    self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    self.setOption(QFileDialog.Option.ShowDirsOnly, False)
    self.setOption(QFileDialog.Option.DontUseCustomDirectoryIcons, False)
    self.setNameFilter('Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)')
    self.setSizeGripEnabled(True)
    self.setOption(QFileDialog.Option.DontResolveSymlinks, True)

  def closeEvent(self, event: QCloseEvent) -> None:
    """Reimplementation that saves the states and closes the dialog. """
    QSettings().setValue('OpenFileDialog/saveState', self.saveState())
    ic("LOL")
    QFileDialog.closeEvent(self, event)

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Reimplementation that saves the states and closes the dialog. """
    ic('LOL')

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Reimplementation that saves the states and closes the dialog. """
    QFileDialog.mouseReleaseEvent(self, event)
