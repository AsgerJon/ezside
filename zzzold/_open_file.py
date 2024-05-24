"""OpenFile provides the open file dialog for the application by
implementing the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog
from attribox import AbstractDescriptor
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from ezside.desc import parseFilter
from ezside.windows import BaseWindow

BASE = BaseWindow
SCOPE = type(QObject)


class OpenFile(AbstractDescriptor):
  """OpenFile provides the open file dialog for the application by
  implementing the descriptor protocol."""

  __name_filter__ = None
  __fallback_filter__ = 'All Files (*)'

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self)
    nameFilter = parseFilter(*args, **kwargs)
    self._setNameFilter(nameFilter)

  def _create(self, instance: BASE, owner: SCOPE) -> None:
    """Creates the FileDialog instance. """
    dialog = QFileDialog()
    dialog.setViewMode(QFileDialog.ViewMode.Detail)
    dialog.setOption(QFileDialog.Option.DontUseNativeDialog)
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setNameFilter(self._getNameFilter())
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
    dialog.fileSelected.connect(instance.openFileSelected)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, dialog)

  def _setNameFilter(self, nameFilter: str) -> None:
    """Set the name filter for the file dialog. """
    self.__name_filter__ = nameFilter

  def _getNameFilter(self, ) -> str:
    """Getter-function for the name filter"""
    return maybe(self.__name_filter__, self.__fallback_filter__)

  def __instance_get__(self, instance: BASE, owner: SCOPE, **kwargs) -> Any:
    """The __instance_get__ method is called when the descriptor is accessed
    from an instance."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    dialog = getattr(instance, pvtName, None)
    if dialog is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._create(instance, owner)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(dialog, QFileDialog):
      return dialog
    e = typeMsg(pvtName, dialog, QFileDialog)
    raise TypeError(e)
