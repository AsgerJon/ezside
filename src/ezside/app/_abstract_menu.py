"""AbstractMenu subclasses QMenu and provides an abstract baseclass for
application menus. Primarily, it adds a relevant type overloads."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import QMenu

from worktoy.base import BaseObject, overload
from worktoy.desc import Field
from worktoy.meta import DispatchException


class _Parsed(BaseObject):
  """_Parsed is a helper class for parsing."""

  __action_arg__ = None
  __shortcut_arg__ = None

  actionArg = Field()
  shortcutArg = Field()

  @actionArg.GET
  def actionArg(self) -> QAction:
    return self.__action_arg__

  @shortcutArg.GET
  def shortcutArg(self) -> QKeySequence:
    return self.__shortcut_arg__

  @overload(QAction, QKeySequence)
  def __init__(self, action: QAction, shortcut: QKeySequence) -> None:
    self.__shortcut_arg__ = shortcut
    self.__action_arg__ = action

  @overload(QKeySequence, QAction)
  def __init__(self, shortcut: QKeySequence, action: QAction) -> None:
    self.__shortcut_arg__ = shortcut
    self.__action_arg__ = action


class AbstractMenu(QMenu):
  """AbstractMenu subclasses QMenu and provides an abstract baseclass for
  application menus. Primarily, it adds a relevant type overloads."""

  def addAction(self, *args, **kwargs) -> None:
    try:
      parsed = _Parsed(*args)
      parsed.actionArg.setShortcut(parsed.shortcutArg)
      QMenu.addAction(self, parsed.actionArg, )
    except DispatchException:
      QMenu.addAction(self, *args, **kwargs)
