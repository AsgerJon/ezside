"""Action subclasses QAction streamlining the creation of QAction
objects."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os.path
from typing import Any

from PySide6.QtGui import QAction, QPixmap, QKeySequence
from PySide6.QtWidgets import QMenu
from worktoy.parse import maybe
from worktoy.text import stringList


class Action(QAction):
  """Action subclasses QAction streamlining the creation of QAction
  objects."""

  @staticmethod
  def _parseIconFile(*args) -> Any:
    """Parses the icon file from the arguments and returns the unused
    arguments."""
    unusedArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if '.png' in arg:
        return arg, [*tempArgs, *unusedArgs]
      unusedArgs.append(arg)
    return None, [*args, ]

  @staticmethod
  def _parseShortCut(*args, ) -> Any:
    """Parses the shortcut from the arguments and returns the unused
    arguments."""
    unusedArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if any([m in arg for m in stringList("""CTRL, SHIFT, ALT""")]):
        return arg, [*tempArgs, *unusedArgs]
      unusedArgs.append(arg)
    return None, [*args, ]

  @staticmethod
  def _parseParent(*args) -> Any:
    """Parses the parent from the arguments and returns the unused
    arguments."""
    unusedArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if isinstance(arg, QMenu):
        return arg, [*tempArgs, *unusedArgs]
      unusedArgs.append(arg)
    return None, [*args, ]

  @staticmethod
  def _parseTitle(*args) -> Any:
    """Parses the title from the arguments and returns the unused
    arguments."""
    unusedArgs = []
    tempArgs = [*args, ]
    while tempArgs:
      arg = tempArgs.pop(0)
      if isinstance(arg, str):
        return arg, [*tempArgs, *unusedArgs]
      unusedArgs.append(arg)
    return None, [*args, ]

  def __init__(self, *args) -> None:
    iconFile, unusedArgs = self._parseIconFile(*args)
    shortCut, unusedArgs = self._parseShortCut(*unusedArgs)
    parent, unusedArgs = self._parseParent(*unusedArgs)
    title, unusedArgs = self._parseTitle(*unusedArgs)
    if title is None or parent is None:
      e = """Unable to parse the title and parent from the arguments."""
      raise ValueError(e)
    QAction.__init__(self, title, parent)
    self.setIcon(maybe(iconFile, 'risitas.png'))
    if shortCut is not None:
      self.setShortcut(shortCut)

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
