"""EZMenu provides a subclass of QMenu and is meant to act as a base class
for menus in the 'ezside' framework. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QWidget
from worktoy.base import BaseObject
from worktoy.desc import Field
from worktoy.text import typeMsg

from ezside.app import AppField
from ezside.app.menus import EZAction
from ezside.utils import parseParent


class _InitMenu(BaseObject):
  """Instances of this class are used in the __init__ methods of the
  EZMenu class. """

  __menu_name__ = None

  menuName = Field()

  @menuName.GET
  def _getMenuName(self) -> str:
    """Getter-function for the menuName."""
    if self.__menu_name__ is None:
      e = """The required menuName has not been set. """
      raise AttributeError(e)
    if isinstance(self.__menu_name__, str):
      return self.__menu_name__
    e = typeMsg('menuName', self.__menu_name__, str)
    raise TypeError(e)

  def __init__(self, menuName: str) -> None:
    self.__menu_name__ = menuName


class EZMenu(QMenu):
  """EZMenu provides a subclass of QMenu and is meant to act as a base class
  for menus in the 'ezside' framework. """

  app = AppField()

  def __init__(self, *args) -> None:
    parent, posArgs = parseParent(*args)
    parsed = _InitMenu(*posArgs)
    name = parsed.menuName
    if not isinstance(name, str):
      e = typeMsg('menuName', name, str)
      raise TypeError(e)
    if parent is None:
      QMenu.__init__(self, name)
    elif isinstance(parent, QWidget):
      QMenu.__init__(self, name, parent)
    else:
      e = typeMsg('parent', parent, QWidget)
      raise TypeError(e)

  @abstractmethod
  def initMenu(self, *args, **kwargs) -> None:
    """Abstract method for initiating the menu. Subclasses should implement
    this method that creates and adds instances of EZAction. """

  def addAction(self, *args) -> None:
    """Adds an action to the menu. """
    for arg in args:
      if isinstance(arg, EZAction):
        return QMenu.addAction(self, arg)
    e = typeMsg('args', args, EZAction)
    raise TypeError(e)
