"""Action subclasses QAction streamlining the creation of QAction
objects."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os.path

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QPixmap, QKeySequence, QIcon
from PySide6.QtWidgets import QMenu, QMainWindow
from icecream import ic
from worktoy.text import typeMsg

from ezside.parser import ActionParser, IconParser

ic.configureOutput(includeContext=True)


class EZAction(QAction):
  """EZAction subclasses QAction streamlining the creation of QAction
  objects."""

  def __init__(self, *args) -> None:
    parseArgs = []
    for arg in args:
      if isinstance(arg, QObject):
        if any([isinstance(i, QObject) for i in parseArgs]):
          continue
        parseArgs.append(arg)
      elif isinstance(arg, str):
        if len([i for i in parseArgs if isinstance(i, str)]) < 2:
          parseArgs.append(arg)
    parsed = ActionParser(*parseArgs)
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
