"""SelectDir provides a dialog for selecting an existing directory. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QFileDialog


class DirectoryDialog(QFileDialog):
  """SelectDir provides a dialog for selecting an existing directory. """

  def __init__(self, parent=None) -> None:
    QFileDialog.__init__(self, parent)
    self.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    self.setFileMode(QFileDialog.FileMode.Directory)
    self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    self.setOption(QFileDialog.Option.ShowDirsOnly, True)
