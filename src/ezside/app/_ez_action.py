"""Action subclasses QAction streamlining the creation of QAction
objects."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, QCoreApplication
from PySide6.QtGui import QAction, QPixmap, QKeySequence, QIcon
from icecream import ic
from worktoy.desc import Field
from worktoy.text import monoSpace

if TYPE_CHECKING:
  from ezside.app import App

ic.configureOutput(includeContext=True)


class EZAction(QAction):
  """EZAction subclasses QAction streamlining the creation of QAction
  objects."""

  app = Field()

  @app.GET
  def _getApp(self) -> App:
    """Getter-function for the app."""
    app = QCoreApplication.instance()
    if getattr(app, '__ezside_app__', None) is None:
      e = """%s requires the running instance of QCoreApplication to be an 
      instance of the ezside.app.App class, but received %s!"""
      raise TypeError(monoSpace(e % (self.__class__.__name__, app)))
    if TYPE_CHECKING:
      assert isinstance(app, App)
    return app

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QObject):
        QAction.__init__(self, arg)
        break
    else:
      QAction.__init__(self)
    strArgs = [arg for arg in args if isinstance(arg, str)]
    name, shortCut, fid = [*strArgs, None, None, None][:3]
    iconPath = self.app.getIconFile(name)
    pix = QPixmap(iconPath)
    QAction.setIcon(self, QIcon(pix))
    QAction.setText(self, name)
    keySequence = QKeySequence.fromString(shortCut)
    if not keySequence.isEmpty():
      QAction.setShortcut(self, keySequence)

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

  def __str__(self, ) -> str:
    """String representation"""
    return """%s(%s)""" % (self.__class__.__name__, self.text())
