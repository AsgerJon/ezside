"""ParseMenu is a helper function which subclasses 'BaseObject' and thus
implements function overloading. Since metaclass conflicts prevent
implementing the 'BaseObject' class as a second base class with 'QObject'
being the first, classes like 'ParseMenu' allows the 'QObject' classes to
take advantage of the function overloading in the 'BaseObject' class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from worktoy.desc import Field
from PySide6.QtGui import QIcon, QPixmap, QKeySequence

from typing import Never

from worktoy.meta import BaseObject, overload

from worktoy.meta import BaseObject

from ezside.parser import AbstractParser


class MenuParser(AbstractParser):
  """This class lets the 'QObject' classes take advantage of the function
  overloading in the 'BaseObject' class. """

  __menu_title__ = None
  title = Field()

  @title.SET
  def _setTitle(self, menuTitle: str) -> None:
    """Setter-function for the title."""
    self.__menu_title__ = menuTitle

  @title.GET
  def _getTitle(self) -> str:
    """Getter-function for the title."""
    return self.__menu_title__

  @title.DELETE
  def _illegalAccessor(self, *_) -> Never:
    """This function should never be called."""
    e = """The 'parent' and 'title' fields are read-only!"""
    raise TypeError(e)

  @overload(str, QWidget)
  def __init__(self, title: str, parent: QWidget) -> None:
    """Initializes the menu."""
    self.title = title
    self.parent = parent

  @overload(QWidget, str)
  def __init__(self, parent: QWidget, title: str) -> None:
    """Initializes the menu."""
    self.title = title
    self.parent = parent

  @overload(str)
  def __init__(self, title: str) -> None:
    """Initializes the menu."""
    self.title = title

  @overload(QWidget)
  def __init__(self, parent: QWidget) -> None:
    """Initializes the menu."""
    self.parent = parent
