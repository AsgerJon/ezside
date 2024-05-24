"""Layout provides a descriptor for the descriptor of the layout. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QLayout
from attribox import AttriBox
from vistutils.fields import EmptyField

from ezside.app import EZDesc
from ezside.core import ORIENTATION, \
  parseOrientation, \
  HORIZONTAL, \
  VERTICAL, \
  parseSpacing, parseMargins
from ezside.layouts import CoreGridLayout, CoreHLayout, CoreVLayout

if TYPE_CHECKING:
  from ezside.windows import BaseWindow as Win


class Layout(EZDesc):
  """Layout provides a descriptor for the descriptor of the layout. """

  __horizontal_orientation__ = None
  __vertical_orientation__ = None

  orientation = EmptyField()
  horizontal = EmptyField()
  vertical = EmptyField()

  spacing = AttriBox[int]()

  @horizontal.GET
  def _getHorizontal(self) -> bool:
    """Gets the horizontal orientation."""
    return True if self.__horizontal_orientation__ else False

  @horizontal.SET
  def _setHorizontal(self, value: bool) -> None:
    """Sets the horizontal orientation."""
    self.__horizontal_orientation__ = True if value else False

  @vertical.GET
  def _getVertical(self) -> bool:
    """Gets the vertical orientation."""
    return True if self.__vertical_orientation__ else False

  @vertical.SET
  def _setVertical(self, value: bool) -> None:
    """Sets the vertical orientation."""
    self.__vertical_orientation__ = True if value else False

  @orientation.GET
  def _getOrientation(self) -> ORIENTATION:
    """Gets the orientation."""
    if self.horizontal and self.vertical:
      return VERTICAL | HORIZONTAL
    if self.horizontal:
      return HORIZONTAL
    if self.vertical:
      return VERTICAL
    return VERTICAL | HORIZONTAL

  @orientation.SET
  def _setOrientation(self, value: ORIENTATION) -> None:
    """Sets the orientation."""
    self.horizontal = True if value == HORIZONTAL else False
    self.vertical = True if value == VERTICAL else False

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Layout."""
    EZDesc.__init__(self, *args, **kwargs)
    self.orientation = parseOrientation(*args, **kwargs)
    self.spacing = parseSpacing(*args, **kwargs)
    self.contentMargins = parseMargins(*args, **kwargs)

  def getContentClass(self) -> type:
    """Returns the content class."""
    if self.horizontal == self.vertical:
      return CoreGridLayout
    if self.horizontal:
      return CoreHLayout
    if self.vertical:
      return CoreVLayout

  def create(self, instance: Win, owner: type, **kwargs) -> QLayout:
    """Create the content."""
    parent = instance.parent()
    return self.getContentClass()()
