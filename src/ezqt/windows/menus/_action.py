"""Action subclasses QAction and customizes the instantiation process."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QAction, QKeySequence
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezqt.windows.menus.icons import getIcon
from ezqt.windows.menus.shortcuts import getShortcut

ic.configureOutput(includeContext=True, )


class Action(QAction):
  """Action subclasses QAction and customizes the instantiation process."""

  def __init__(self, *args, **kwargs) -> None:
    if isinstance(args[0], str):
      name = args[0]
      QAction.__init__(self, name)
      self._name = name
    elif isinstance(args[0], QAction):
      self._name = args[0].text() or 'LOL'
    else:
      e = typeMsg('action', args[0], QAction)
      raise TypeError(e)
    self.__icon_path__ = None

  def setIconPath(self, iconPath: str) -> None:
    """Sets the icon for the action."""
    self.__icon_path__ = iconPath

  def setupAction(self, ) -> None:
    """Sets up the action."""
    shortcut = getShortcut(self._name)
    if isinstance(shortcut, QKeySequence):
      self.setShortcut(shortcut)

  def setupIcon(self) -> str:
    """Sets up the icon for the action."""
    icon = getIcon(self._name)
    if icon:
      self.setIconPath(icon)
      return icon

  def __str__(self, ) -> str:
    """Returns the name of the action."""
    name = self._name
    shortcut = self.shortcut().toString()
    menu = self.menu().title()
    if shortcut:
      return '%s | %s %s' % (menu, name, shortcut)
    return '%s | %s' % (menu, name)

  def __repr__(self, ) -> str:
    """Returns the name of the action."""
    return self._name
