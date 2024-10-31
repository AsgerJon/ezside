"""Action subclasses QAction streamlining the creation of QAction
objects."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Never

from PySide6.QtCore import QObject, QCoreApplication
from PySide6.QtGui import QAction, QPixmap, QKeySequence, QIcon
from icecream import ic
from worktoy.base import BaseObject, overload
from worktoy.desc import Field, AttriBox
from worktoy.text import monoSpace, typeMsg
from ezside.app import AppField
from ezside.app.menus import EZIcon
from ezside.utils import parseParent

if TYPE_CHECKING:
  from ezside.app import App

ic.configureOutput(includeContext=True)


class _InitAction(BaseObject):
  """Instances of this class are used in the __init__ methods of the
  EZAction class. """

  __action_name__ = None
  __short_cut__ = None
  __action_icon__ = None

  actionName = Field()
  shortCut = Field()
  icon = Field()

  @shortCut.GET
  def _getShortCut(self) -> QKeySequence:
    """Getter-function for the shortCut."""
    if self.__short_cut__ is None:
      return QKeySequence()
    if isinstance(self.__short_cut__, str):
      return QKeySequence.fromString(self.__short_cut__)
    if isinstance(self.__short_cut__, QKeySequence):
      return self.__short_cut__
    e = typeMsg('shortCut', self.__short_cut__, str)
    raise TypeError(e)

  @shortCut.SET
  def _setShortCut(self, value: Any) -> None:
    """Setter-function for the shortCut."""
    if isinstance(value, (str, QKeySequence)):
      self.__short_cut__ = value
    else:
      e = typeMsg('shortCut', value, str)
      raise TypeError(e)

  @actionName.GET
  def _getActionName(self) -> str:
    """Getter-function for the actionName."""
    if self.__action_name__ is None:
      e = """The required actionNAme has not been set. """
      raise AttributeError(e)
    if isinstance(self.__action_name__, str):
      return self.__action_name__
    e = typeMsg('actionName', self.__action_name__, str)
    raise TypeError(e)

  @actionName.SET
  def _setActionName(self, value: Any) -> None:
    """Setter-function for the actionName."""
    if isinstance(value, str):
      self.__action_name__ = value
    else:
      e = typeMsg('actionName', value, str)
      raise TypeError(e)

  @icon.GET
  def _getIcon(self) -> QIcon:
    """Getter-function for the icon."""
    if self.__action_icon__ is None:
      return QIcon()
    if isinstance(self.__action_icon__, QIcon):
      return self.__action_icon__
    e = typeMsg('icon', self.__action_icon__, QIcon)
    raise TypeError(e)

  @overload(str, str, str)
  def __init__(self, actionName: str, shortCut: str, icon: str) -> None:
    self.actionName = actionName
    self.shortCut = shortCut
    self.icon = EZIcon(icon)

  @overload(str, QKeySequence)
  def __init__(self,
               actionName: str,
               shortCut: QKeySequence,
               icon: str) -> None:
    self.actionName = actionName
    self.shortCut = shortCut
    self.icon = EZIcon(icon)

  @overload(str, str)
  def __init__(self, actionName: str, shortCut: str) -> None:
    self.actionName = actionName
    self.shortCut = shortCut
    self.icon = EZIcon(actionName)

  @overload(str, QKeySequence)
  def __init__(self, actionName: str, shortCut: QKeySequence) -> None:
    self.actionName = actionName
    self.shortCut = shortCut
    self.icon = EZIcon(actionName)

  @overload(str)
  def __init__(self, actionName: str) -> None:
    self.actionName = actionName
    self.icon = EZIcon(actionName)

  @overload()
  def __init__(self, ) -> Never:
    """At least the name is required"""
    e = """Missing required argument: 'actionName'!"""
    raise ValueError(monoSpace(e))


class EZAction(QAction):
  """EZAction subclasses QAction streamlining the creation of QAction
  objects."""

  app = AppField()

  def __init__(self, *args) -> None:
    parent, posArgs = parseParent(*args)
    if parent is None:
      QAction.__init__(self)
    elif isinstance(parent, QObject):
      QAction.__init__(self, parent)
    else:
      e = typeMsg('parent', parent, QObject)
      raise TypeError(e)
    parsed = _InitAction(*posArgs)
    name, shortCut = parsed.actionName, parsed.shortCut
    icon = EZIcon(name)
    self.setText(name)
    self.setShortcut(shortCut)
    self.setIcon(icon.value)
