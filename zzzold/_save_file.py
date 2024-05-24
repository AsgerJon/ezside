"""OpenFile provides the open file dialog for the application by
implementing the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog
from attribox import AbstractDescriptor
from vistutils.parse import maybe

from ezside.desc import parseFilter
from ezside.dialogs import OpenFile
from ezside.windows import BaseWindow

BASE = BaseWindow
SCOPE = type(QObject)


class SaveFile(OpenFile):
  """SaveFile provides a descriptor class for creating a file dialog for
  save files. """

  __name_filter__ = None
  __fallback_filter__ = 'All Files (*)'

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self)
    nameFilter = parseFilter(*args, **kwargs)
    self._setNameFilter(maybe(nameFilter, self.__fallback_filter__))

  def _create(self, instance: BASE, owner: SCOPE) -> None:
    """Creates the FileDialog instance. """
    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.ViewMode.Detail)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setNameFilter(self._getNameFilter())
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    dialog.fileSelected.connect(instance.saveFileSlot)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)
