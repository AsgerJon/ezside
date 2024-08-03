"""AbstractParser provides an abstract base class for the parser classes
that inherit the 'BaseObject' class, which provides powerful features like
function overloading. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from worktoy.meta import BaseObject, overload
from worktoy.desc import Field


class AbstractParser(BaseObject):
  """This class lets the 'BaseObject' classes take advantage of the function
  overloading in the 'BaseObject' class. """

  __parent_widget__ = None

  parent = Field()

  @parent.SET
  def _setParent(self, parentWidget: QWidget) -> None:
    """Setter-function for the parent."""
    self.__parent_widget__ = parentWidget

  @parent.GET
  def _getParent(self) -> QWidget:
    """Getter-function for the parent."""
    return self.__parent_widget__
