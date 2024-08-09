"""ParseAction parses arguments related to QAction. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import Any

from PySide6.QtCore import QObject, QSize
from PySide6.QtWidgets import QWidget
from worktoy.desc import Field
from PySide6.QtGui import QIcon, QPixmap, QKeySequence, QImage

from worktoy.meta import BaseObject, overload
from worktoy.text import typeMsg

from ezside.parser import AbstractParser, IconParser


class ActionParser(AbstractParser):
  """This class implements overloading in its functions through the
  'BaseObject' class. Since metaclass conflicts are not allowed,
  this uses the function overloading to collect values from arguments. """

  __action_title__ = None
  __action_icon__ = None
  __action_shortcut__ = None
  __icon_parser__ = None

  title = Field()
  icon = Field()
  shortCut = Field()

  @title.SET
  def _setTitle(self, actionTitle: str) -> None:
    """Setter-function for the title."""
    self.__action_title__ = actionTitle

  @shortCut.SET
  @overload(str)
  def _setShortCut(self, shortCut: str) -> None:
    """Setter-function for the shortcut."""
    keySequence = QKeySequence.fromString(shortCut)
    if keySequence.isEmpty():
      return
    self.__action_shortcut__ = keySequence

  @shortCut.SET
  @overload(QKeySequence)
  def _setShortCut(self, shortCut: QKeySequence) -> None:
    """Setter-function for the shortcut."""
    self.__action_shortcut__ = shortCut

  @title.GET
  def _getTitle(self) -> str:
    """Getter-function for the title."""
    return self.__action_title__

  @shortCut.GET
  def _getShortCut(self) -> QKeySequence:
    """Getter-function for the shortcut."""
    return self.__action_shortcut__

  #  Icon retrieval
  @icon.GET
  def _getIcon(self, **kwargs) -> QIcon:
    """Getter-function for the icon."""
    if self.__icon_parser__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.__icon_parser__ = IconParser(self.title.lower())
      return self._getIcon(_recursion=True)
    if isinstance(self.__icon_parser__, IconParser):
      return self.__icon_parser__.icon
    e = typeMsg('iconParser', self.__icon_parser__, IconParser)
    raise TypeError(e)

  @icon.SET
  def _setIcon(self, newIcon: Any) -> None:
    """Setter-function for the icon."""
    if isinstance(newIcon, str):
      self.__icon_parser__ = IconParser(newIcon.lower())
    elif isinstance(newIcon, QPixmap):
      iconPath = IconParser.getIconPath()
      iconFileName = '%s.png' % self.title.lower()
      for item in os.listdir(iconPath):
        if self.title.lower() in item:
          digNum = 1
          while iconFileName[-digNum].isnumeric():
            if int(iconFileName[-digNum]):
              digNum += 1
              continue
            break
          num = int(iconFileName[-digNum:]) + 1
          iconFileName = '%s%s.png' % (self.title.lower(), num)
          break
      else:
        iconFileName = '%s00.png' % self.title.lower()
      newIcon.save(os.path.join(iconPath, iconFileName))
      self.__icon_parser__ = IconParser(iconFileName.replace('.png', ''))
      return
    if isinstance(newIcon, QIcon):
      return self._setIcon(newIcon.pixmap(QSize(128, 128)))
    if isinstance(newIcon, QImage):
      return self._setIcon(QPixmap.fromImage(newIcon))

  #  __init__ overloads

  @overload(QObject)
  def __init__(self, parentWidget: QObject) -> None:
    """Constructor for the ActionParse class."""
    self.parent = parentWidget

  @overload(QObject, str)
  def __init__(self, parentWidget: QObject, *args) -> None:
    """Constructor for the ActionParse class."""
    self.__init__(parentWidget)
    self.__init__(*args)

  @overload(QObject, str, str)
  def __init__(self, parentWidget: QWidget, *args) -> None:
    """Constructor for the ActionParse class."""
    self.parent = parentWidget
    self.__init__(*args)

  @overload(str)
  def __init__(self, actionTitle: str, ) -> None:
    """Constructor for the ActionParse class."""
    self.title = actionTitle

  @overload(str, str)
  def __init__(self, actionTitle: str, shortCut: str, ) -> None:
    """Constructor for the ActionParse class."""
    self.title = actionTitle
    self.shortCut = shortCut
