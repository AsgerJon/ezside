"""SaveFile provides a custom implementation of the save file dialog."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog
from worktoy.desc import AttriBox


class SaveFileDialog(QFileDialog):
  """SaveFile provides a custom implementation of the save file dialog."""

  def __init__(self, parent: QObject = None) -> None:
    QFileDialog.__init__(self, parent)
    self.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    self.setFileMode(QFileDialog.FileMode.AnyFile)
    self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    self.setOption(QFileDialog.Option.ShowDirsOnly, False)
    self.setOption(QFileDialog.Option.DontConfirmOverwrite, False)
