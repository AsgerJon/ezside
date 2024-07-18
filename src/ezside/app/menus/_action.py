"""Action subclasses QAction"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TypeAlias

from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QKeySequence, QIcon
from worktoy.text import stringList, monoSpace

ParsedArgs: TypeAlias = tuple[object, tuple[object], dict[str, object]]


class Action(QAction):
  """Action subclasses QAction"""

  __action_title__ = None
  __keyboard_shortcut__ = None
  __action_icon__ = None
  __action_parent__ = None

  @staticmethod
  def _resolveIcon(name: str) -> QIcon:
    """Resolves the icon from the name. """
    here = os.path.dirname(__file__)
    iconDir = os.path.join(here, '../iconfiles')
    if not os.path.exists(iconDir):
      e = """Icon directory: '%s' not found!""" % iconDir
      raise FileNotFoundError(monoSpace(e))
    if not os.path.isdir(iconDir):
      e = """Icon directory: '%s' is not a directory!""" % iconDir
      raise NotADirectoryError(monoSpace(e))
    name = name.lower().replace(' ', '').replace('_', '')
    for file in os.listdir(iconDir):
      icon = file.lower().replace(' ', '').replace('_', '').split('.')[0]
      if icon == name:
        return QIcon(os.path.join(iconDir, file))

  @staticmethod
  def _parseShortcut(*args, **kwargs) -> ParsedArgs:
    shortcutKeys = stringList("""shortcut, keyboard, shortcutKey""")
    tempArgs = [*args, ]
    for key in shortcutKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          keySequence = QKeySequence.fromString(val)
          if not keySequence.isEmpty():
            return keySequence, (*tempArgs,), {**kwargs, }
    else:
      unusedArgs = []
      while tempArgs:
        arg = tempArgs.pop(0)
        if isinstance(arg, str):
          keySequence = QKeySequence.fromString(arg)
          if not keySequence.isEmpty():
            while tempArgs:
              unusedArgs.append(tempArgs.pop(0))
            return keySequence, (*unusedArgs,), {**kwargs, }
        unusedArgs.append(arg)
      else:
        return QKeySequence.fromString(''), (*unusedArgs,), {**kwargs, }

  @classmethod
  def _parseIcon(cls, *args, **kwargs) -> ParsedArgs:
    tempArgs = [*args, ]
    iconKeys = stringList("""icon, actionIcon, ico""")
    for key in iconKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          icon = cls._resolveIcon(val)
          if isinstance(icon, QIcon):
            return icon, (*tempArgs,), {**kwargs, }
    else:
      unusedArgs = []
      while tempArgs:
        arg = tempArgs.pop(0)
        if isinstance(arg, str):
          icon = cls._resolveIcon(arg)
          if isinstance(icon, QIcon):
            while tempArgs:
              unusedArgs.append(tempArgs.pop(0))
            return icon, (*unusedArgs,), {**kwargs, }
      else:
        return cls._resolveIcon('risitas'), (*unusedArgs,), {**kwargs, }

  @classmethod
  def _parseTitle(cls, *args, **kwargs) -> ParsedArgs:
    tempArgs = [*args, ]
    titleKeys = stringList("""title, actionTitle""")
    for key in titleKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          return val, (*tempArgs,), {**kwargs, }
    else:
      unusedArgs = []
      while tempArgs:
        arg = tempArgs.pop(0)
        if isinstance(arg, str):
          while tempArgs:
            unusedArgs.append(tempArgs.pop(0))
          return arg, (*unusedArgs,), {**kwargs, }
        unusedArgs.append(arg)
      else:
        e = """Action requires a title!"""
        raise ValueError(monoSpace(e))

  @classmethod
  def _parseParent(cls, *args, **kwargs) -> ParsedArgs:
    tempArgs = [*args, ]
    parentKeys = stringList("""parent, actionParent, parentMenu""")
    for key in parentKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, QAction):
          return val, (*tempArgs,), {**kwargs, }
    else:
      unusedArgs = []
      for arg in args:
        if isinstance(arg, QAction):
          return arg, (*tempArgs,), {**kwargs, }
      else:
        return None, (*tempArgs,), {**kwargs, }

  def __init__(self, *args, **kwargs) -> None:
    __action_title__ = None
    __keyboard_shortcut__ = None
    __action_icon__ = None
    __action_parent__ = None
    title, args, kwargs = self._parseTitle(*args, **kwargs)
    shortcut, args, kwargs = self._parseShortcut(*args, **kwargs)
    icon, args, kwargs = self._parseIcon(*args, **kwargs)
    parent, args, kwargs = self._parseParent(*args, **kwargs)
    QAction.__init__(self, )
    if isinstance(title, str):
      self.__action_title__ = title
    if isinstance(shortcut, QKeySequence):
      self.__action_title__ = shortcut
    if isinstance(icon, QIcon):
      self.__action_title__ = icon
    if isinstance(parent, QObject):
      self.__action_title__ = parent

  def initUi(self) -> None:
    """Initialize the user interface for the widget. """
    self.setText(self.__action_title__)
    self.setShortcut(self.__keyboard_shortcut__)
    self.setIcon(self.__action_icon__)
    self.setParent(self.__action_parent__)
