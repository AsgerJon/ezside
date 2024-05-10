"""_BaseWidgetPrivates provides a base class for the BaseWidget class
that provides the private attributes and functionality."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from enum import EnumType
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QWidget
from icecream import ic
from vistutils.text import monoSpace, stringList
from vistutils.waitaminute import typeMsg

from ezside.core import resolveEnum
from morevistutils import hasAbstractMethod

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class _BaseWidgetPrivates(QWidget):
  """_BaseWidgetPrivates provides a base class for the BaseWidget class
  that provides the private attributes and functionality."""

  @classmethod
  @abstractmethod
  def staticStyles(cls, ) -> dict[str, Any]:
    """Returns the base styles for the widget. The method should return a
    dictionary mapping style names to style values. """

  @classmethod
  @abstractmethod
  def dynStyles(cls, ) -> dict[str, Any]:
    """Returns the dynamic styles for the widget. The method should return a
    dictionary mapping style names to style values. """

  def getStyle(self, name) -> Any:
    """Returns the style value for the given style name. """
    return self.dynStyles().get(name, self.staticStyles().get(name, ))


