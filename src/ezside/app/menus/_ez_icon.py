"""EZIcon is responsible for providing icons for a number of common names.
By encapsulating this functionality in a class, themes can easily be
swapped."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import Any, TYPE_CHECKING
from warnings import warn

from PySide6.QtGui import QIcon
from worktoy.base import BaseObject
from worktoy.keenum import KeeNum, auto, KeeNumMeta
from worktoy.text import monoSpace

from ezside.app import AppField
from moreworktoy.io import validateFile


class _InitIcon(BaseObject):
  """This class encapsulates the actual QIcon file for a given name. """
  app = AppField()
  __active_theme__ = 'base'
  __fallback_name__ = 'risitas'
  __icon_name__ = None
  __q_icon__ = None

  @staticmethod
  def _getCommonImgExtensions() -> list[str]:
    """This method returns a list of common image extensions. """
    return [
        '.jpeg', '.jpg', '.png', '.gif', '.bmp',
        '.tiff', '.tif', '.webp', '.heic', '.svg'
    ]

  @classmethod
  def _getIconFile(cls, name: str, **kwargs) -> str:
    """This method resolves the icon file for a given name. """
    imgExt = cls._getCommonImgExtensions()
    if name in imgExt:
      if kwargs.get('_recursion', False):
        raise RecursionError
      return cls._getIconFile(cls.__fallback_name__, _recursion=True)
    for item in os.listdir(cls.app.iconDir):
      if item.startswith(name):
        for ext in imgExt:
          if item.endswith(ext):
            fid = os.path.join(cls.app.iconDir, item)
            validateFile(fid)
            break
    else:
      if kwargs.get('_recursion', False):
        raise RecursionError
      return cls._getIconFile(cls.__fallback_name__, _recursion=True)

  def _loadIcon(self, name: str) -> QIcon:
    """This method loads the icon for a given name. """

    return QIcon(self._getIconFile(name))

  def __init__(self, name: str) -> None:
    self.__icon_name__ = name


class _EZIconMeta(KeeNumMeta):
  """This metaclass provides the metaclass for the EZIcon class. It
  subclasses the KeeNumMeta class, the baseclass for the KeeNum class.
  This subclass implements a fallback icon when attempting to access a
  missing icon. """

  def __getattr__(cls, key: str) -> Any:
    """This method returns the QIcon for a given name. """
    w = """Unable to find icon for: '%s' falling back to: '%s'."""
    fallback = getattr(cls, '__fallback_icon__', None)
    if fallback is None:
      return object.__getattribute__(cls, key)
    warn(monoSpace(w % (key, fallback)))
    return fallback


class EZIcon(metaclass=_EZIconMeta):
  """EZIcon is responsible for providing icons for a number of common names.
  By encapsulating this functionality in a class, themes can easily be
  swapped."""

  CONDA = auto(_InitIcon('about_conda'))
  PYSIDE6 = auto(_InitIcon('about_pyside6'))
  PYTHON = auto(_InitIcon('about_python'))
  QT = auto(_InitIcon('about_qt'))
  ADD = auto(_InitIcon('add'))
  COPY = auto(_InitIcon('copy'))
  CUT = auto(_InitIcon('cut'))
  DEBUG = auto(_InitIcon('debug'))
  DOC = auto(_InitIcon('documentation'))
  EDIT = auto(_InitIcon('edit_menu'))
  EXIT = auto(_InitIcon('exit'))
  FILES = auto(_InitIcon('files'))
  HELP = auto(_InitIcon('help_menu'))
  LOCK = auto(_InitIcon('locked'))
  MIC = auto(_InitIcon('microphone'))
  NEW = auto(_InitIcon('new'))
  OPEN = auto(_InitIcon('open'))
  PASTE = auto(_InitIcon('paste'))
  PRF = auto(_InitIcon('preferences'))
  REDO = auto(_InitIcon('redo'))
  SAVE = auto(_InitIcon('save'))
  SAVEAS = auto(_InitIcon('save_as'))
  SCREENSHOT = auto(_InitIcon('screen_shot'))
  SELECTALL = auto(_InitIcon('select_all'))
  UNDO = auto(_InitIcon('undo'))
  UNLOCK = auto(_InitIcon('unlocked'))

  if TYPE_CHECKING:
    def __init__(self, *args, **kwargs) -> None:
      pass
