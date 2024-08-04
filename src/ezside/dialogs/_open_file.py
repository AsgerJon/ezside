"""OpenFile dialog provides a dialog for selecting an existing file. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QFileDialog


class OpenFileDialog(QFileDialog):
  """OpenFile dialog provides a dialog for selecting an existing file. """

  def __init__(self, parent=None) -> None:
    QFileDialog.__init__(self, parent)
    self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    self.setFileMode(QFileDialog.FileMode.ExistingFile)
    self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    self.setOption(QFileDialog.Option.ShowDirsOnly, False)
