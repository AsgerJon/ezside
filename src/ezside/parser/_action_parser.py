"""ParseAction parses arguments related to QAction. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
from worktoy.desc import Field
from PySide6.QtGui import QIcon, QPixmap, QKeySequence

from worktoy.meta import BaseObject, overload

from ezside.parser import AbstractParser


class ActionParser(AbstractParser):
  """This class implements overloading in its functions through the
  'BaseObject' class. Since metaclass conflicts are not allowed,
  this uses the function overloading to collect values from arguments. """

  __action_title__ = None
  __action_icon__ = None
  __action_shortcut__ = None

  title = Field()
  icon = Field()
  shortCut = Field()

  @title.SET
  def _setTitle(self, actionTitle: str) -> None:
    """Setter-function for the title."""
    self.__action_title__ = actionTitle

  @icon.SET
  @overload(str)
  def _setIcon(self, iconFile: str, **kwargs) -> None:
    """Setter-function for the icon file."""
    if not os.path.isabs(iconFile):
      if kwargs.get('_recursion', False):
        raise RecursionError
      here = os.path.dirname(os.path.abspath(__file__))
      iconFile = os.path.join(here, '..', 'app', 'icons', iconFile)
      iconFile = os.path.normpath(iconFile)
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

  @overload(QObject)
  def __init__(self, parentWidget: QObject) -> None:
    """Constructor for the ActionParse class."""
    self.parent = parentWidget

  @overload(QObject, str, str, str)
  def __init__(self,
               parentWidget: QWidget,
               actionTitle: str,
               shortCut: str,
               iconFile: str, ) -> None:
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

  @overload(QObject, str)
  def __init__(self, parentWidget: QObject, actionTitle: str) -> None:
    """Constructor for the ActionParse class."""
    self.title = actionTitle
    self.__init__(parentWidget)
