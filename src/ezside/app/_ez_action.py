"""Action subclasses QAction streamlining the creation of QAction
objects."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os.path

from PySide6.QtGui import QAction, QPixmap, QKeySequence
from PySide6.QtWidgets import QMenu, QMainWindow
from icecream import ic

from ezside.parser import ActionParser

ic.configureOutput(includeContext=True)


class EZAction(QAction):
  """EZAction subclasses QAction streamlining the creation of QAction
  objects."""

  def __init__(self, *args) -> None:
    parsed = ActionParser(*args)
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

  def __str__(self, ) -> str:
    """String representation"""
    return QAction.text(self)
