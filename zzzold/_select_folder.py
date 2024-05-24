"""SelectFolder provides the folder selection dialog for the application by
implementing the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog

from ezside.dialogs import OpenFile
from ezside.windows import BaseWindow

BASE = BaseWindow
SCOPE = type(QObject)


class SelectFolder(OpenFile):
  """SelectFolder provides the folder selection dialog for the application by
  implementing the descriptor protocol."""

  def _create(self, instance: BASE, owner: SCOPE) -> None:
    """Creates the FileDialog instance. """
    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.ViewMode.Detail)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    dialog.fileSelected.connect(instance.folderSelected)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)
