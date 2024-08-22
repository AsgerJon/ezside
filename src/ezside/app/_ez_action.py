"""Action subclasses QAction streamlining the creation of QAction
objects."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os.path

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QPixmap, QKeySequence, QIcon
from PySide6.QtWidgets import QMenu, QMainWindow, QWidget
from icecream import ic
from worktoy.text import typeMsg, stringList

from ezside.parser import ActionParser, IconParser

ic.configureOutput(includeContext=True)


class EZAction(QAction):
  """EZAction subclasses QAction streamlining the creation of QAction
  objects."""

  @classmethod
  def _getRoot(cls, here: str = None) -> str:
    """Returns path to root directory"""
    if here is None:
      here = os.path.dirname(os.path.abspath(__file__))
    items = os.listdir(here)
    rootItems = stringList("""src, README.md ,LICENSE""")
    for item in rootItems:
      if item not in items:
        parentDir = cls._getRoot(os.path.join(here, '..'))
        return cls._getRoot(os.path.normpath(parentDir))
    else:
      return here

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QObject):
        QAction.__init__(self, arg)
        break
    else:
      QAction.__init__(self)
    strArgs = [arg for arg in args if isinstance(arg, str)]
    name, shortCut, fid = [*strArgs, None, None, None][:3]
    iconPath = os.path.join(self._getRoot(), 'etc', 'icons')
    name2 = name.lower()
    name2 = name2.replace(' ', '')
    name2 = name2.replace('_', '')
    for item in os.listdir(iconPath):
      item2 = item.lower()
      item2 = item2.replace(' ', '')
      item2 = item2.replace('_', '')
      if name2 in item2:
        QAction.setIcon(self, QIcon(os.path.join(iconPath, item)))
        break
    else:
      QAction.setIcon(self, QIcon(os.path.join(iconPath, 'risitas.png')))
    QAction.setText(self, name)
    keySequence = QKeySequence.fromString(shortCut)
    if not keySequence.isEmpty():
      QAction.setShortcut(self, keySequence)

  def setIcon(self, iconParser: IconParser = None) -> None:
    """Reimplementation supporting receiving a file name"""

    if isinstance(iconParser, IconParser):
      return QAction.setIcon(self, iconParser.icon)
    if isinstance(iconParser, (QPixmap, QIcon)):
      return QAction.setIcon(self, iconParser)
    e = typeMsg('iconParser', iconParser, IconParser)
    raise TypeError(e)

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

  def __str__(self, ) -> str:
    """String representation"""
    return QAction.text(self)
