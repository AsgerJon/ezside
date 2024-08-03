"""Action subclasses QAction streamlining the creation of QAction
objects."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os.path

from PySide6.QtGui import QAction, QPixmap, QKeySequence, QIcon
from PySide6.QtWidgets import QMenu, QWidget
from worktoy.desc import Field
from worktoy.meta import BaseObject, overload


class _ActionParse(BaseObject):
  """This class implements overloading in its functions through the
  'BaseObject' class. Since metaclass conflicts are not allowed,
  this uses the function overloading to collect values from arguments. """

  __parent_widget__ = None
  __action_title__ = None
  __action_icon__ = None
  __action_shortcut__ = None

  parent = Field()
  title = Field()
  icon = Field()
  shortCut = Field()

  @parent.SET
  def _setParent(self, parentWidget: QWidget) -> None:
    """Setter-function for the parent."""
    self.__parent_widget__ = parentWidget

  @title.SET
  def _setTitle(self, actionTitle: str) -> None:
    """Setter-function for the title."""
    self.__action_title__ = actionTitle

  @icon.SET
  @overload(str)
  def _setIcon(self, iconFile: str) -> None:
    """Setter-function for the icon file."""
    if not os.path.exists(iconFile):
      e = """Unable to find icon file at: '%s'!""" % iconFile
      raise FileNotFoundError(e)
    if os.path.isdir(iconFile):
      e = """The icon file at: '%s' is a directory!""" % iconFile
      raise IsADirectoryError(e)
    pix = QPixmap(iconFile)
    self.icon = QIcon(pix)

  @icon.SET
  @overload(QIcon)
  def _setIcon(self, icon: QIcon) -> None:
    """Setter-function for the icon."""
    self.__action_icon__ = icon

  @shortCut.SET
  @overload(str)
  def _setShortCut(self, shortCut: str) -> None:
    """Setter-function for the shortcut."""
    self.shortCut = QKeySequence.fromString(shortCut)

  @shortCut.SET
  @overload(QKeySequence)
  def _setShortCut(self, shortCut: QKeySequence) -> None:
    """Setter-function for the shortcut."""
    self.__action_shortcut__ = shortCut

  @parent.GET
  def _getParent(self) -> QWidget:
    """Getter-function for the parent."""
    return self.__parent_widget__

  @title.GET
  def _getTitle(self) -> str:
    """Getter-function for the title."""
    return self.__action_title__

  @icon.GET
  def _getIcon(self) -> QIcon:
    """Getter-function for the icon."""
    return self.__action_icon__

  @shortCut.GET
  def _getShortCut(self) -> QKeySequence:
    """Getter-function for the shortcut."""
    return self.__action_shortcut__

  @overload(QWidget)
  def __init__(self, parentWidget: QWidget) -> None:
    """Constructor for the ActionParse class."""
    self.parent = parentWidget

  @overload(QWidget, str, str, str)
  def __init__(self,
               parentWidget: QWidget,
               actionTitle: str,
               iconFile: str,
               shortCut: str) -> None:
    """Constructor for the ActionParse class."""
    self.title = actionTitle
    self.icon = iconFile
    self.shortCut = shortCut
    self.__init__(parentWidget)

  @overload(str, str, str)
  def __init__(self, actionTitle: str, shortCut: str, iconFile: str) -> None:
    """Constructor for the ActionParse class."""
    self.title = actionTitle
    self.icon = iconFile
    self.shortCut = shortCut


class Action(QAction):
  """Action subclasses QAction streamlining the creation of QAction
  objects."""

  def __init__(self, *args) -> None:
    parsed = _ActionParse(*args)
    if parsed.parent:
      QAction.__init__(self, parsed.parent)
    else:
      QAction.__init__(self)
    if parsed.title:
      self.setText(parsed.title)
    if parsed.icon:
      self.setIcon(parsed.icon)
    if parsed.shortCut:
      self.setShortcut(parsed.shortCut)

  def setIcon(self, *args) -> None:
    """Reimplementation supporting receiving a file name"""
    for arg in args:
      if isinstance(arg, str):
        if '.png' in arg:
          here = os.path.dirname(os.path.abspath(__file__))
          iconFile = os.path.join(here, 'icons', arg)
          if os.path.isfile(iconFile):
            pix = QPixmap(iconFile)
            return QAction.setIcon(self, pix)
    else:
      return QAction.setIcon(self, *args)

  def setShortcut(self, *args) -> None:
    """Reimplementation supporting receiving a string"""
    for arg in args:
      if isinstance(arg, str):
        shortCut = QKeySequence.fromString(arg)
        if shortCut.isEmpty():
          continue
        return QAction.setShortcut(self, shortCut)
    else:
      return QAction.setShortcut(self, *args)

  def setText(self, *args) -> None:
    """Reimplementation supporting receiving a string"""
    for arg in args:
      if isinstance(arg, str):
        return QAction.setText(self, arg)
    else:
      return QAction.setText(self, *args)

  def setParent(self, *args) -> None:
    """Reimplementation supporting receiving a QMenu"""
    for arg in args:
      if isinstance(arg, QMenu):
        return QAction.setParent(self, arg)
    else:
      return QAction.setParent(self, *args)
