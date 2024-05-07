"""Menu provides a simplified menu implementation"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from icecream import ic

from ezside.app import AppSettings
from ezside.app.menus import _AttriMenu

if TYPE_CHECKING:
  pass
ic.configureOutput(includeContext=True, )


class AbstractMenu(_AttriMenu):
  """A class for managing menus in the application."""

  __iter_contents__ = None
  __added_actions__ = None

  hoverText = Signal(str)

  def __init__(self, menuName: str, *args, **kwargs) -> None:
    """Initializes the menu."""
    title = menuName.capitalize()
    QMenu.__init__(self, title)
    self.initStyle()
    self.initUi()
    self.initSignalSlot()

  def initStyle(self, ) -> None:
    """Initialize the style of the menu. Subclasses may implement this
    method to customize the style of the menu. """

  @abstractmethod
  def initUi(self, ) -> None:
    """Initialize the UI of the menu. Subclasses are required to implement
    this method. The method is expected to instantiate the actions. """

  def initSignalSlot(self, ) -> None:
    """Initialize the signal-slot connections. Subclasses may implement this
    method, but generally the menu class is not responsible for handling
    actions just for presenting them. """

  def _getActionList(self) -> list[QAction]:
    """Get the list of actions."""
    if self.__added_actions__ is None:
      self.__added_actions__ = []
    return self.__added_actions__

  def addAction(self, *args) -> QAction:
    """Add an action to the menu."""
    title = args[0]
    name = title.split(' ')
    if len(name) > 1:
      first = '%s%s' % (name[0][0].lower(), name[0][1:])
      rest = [word for word in name[1:]]
      rest = ['%s%s' % (word[0].upper(), word[1:]) for word in rest]
      name = '%s%s' % (first, ''.join(rest))
    else:
      name = name[0].lower()
    settings = AppSettings()
    icon = settings.value('icon/%s' % name, )
    shortcut = settings.value('shortcut/%s' % name, )
    action = QMenu.addAction(self, icon, title, shortcut)
    setattr(self, name, action)
    self._getActionList().append(action)
    return action

  def __iter__(self) -> AbstractMenu:
    """Iterate over the contents of the menu bar."""
    self.__iter_contents__ = [*self._getActionList(), ]
    return self

  def __next__(self, ) -> QAction:
    """Implementation of iteration protocol"""
    try:
      return self.__iter_contents__.pop(0)
    except IndexError:
      raise StopIteration

  def __len__(self) -> int:
    """Return the number of menus in the menu bar."""
    return len(self._getActionList())

  def __contains__(self, other: QAction) -> bool:
    """Check if a menu is in the menu bar."""
    for action in self:
      if action is other:
        return True
    else:
      return False
