"""PushButtonConfig instantiates BoxModel based on few parameters. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from worktoy.base import BaseObject, overload
from worktoy.parse import maybe
from worktoy.desc import Field, AttriBox

from ..core import RGBA, BoxModel, Margin


class PushButtonConfig(BaseObject):
  """This class instantiates BoxModel based on few parameters. """

  __field_name__ = None
  __field_owner__ = None

  __total_width__ = 6
  __fallback_width__ = 1
  __fallback_radius__ = 1
  __border_width__ = None
  __corner_radius__ = None

  fillColor = AttriBox[RGBA](255, 255, 255, 255)
  borderColor = AttriBox[RGBA](0, 0, 0, 255)
  marginWidth = Field()
  borderWidth = Field()
  paddingWidth = Field()
  cornerRadius = Field()

  @borderWidth.GET
  def _getBorderWidth(self) -> int:
    """Returns the border width. """
    return maybe(self.__border_width__, self.__fallback_width__)

  @borderWidth.SET
  def _setBorderWidth(self, value: int) -> None:
    """Sets the border width. """
    self.__border_width__ = value

  @marginWidth.GET
  def _getMarginWidth(self) -> int:
    """Returns the margin width. """
    if TYPE_CHECKING:
      assert isinstance(self.borderWidth, int)
    remainder = self.__total_width__ - self.borderWidth
    return int((remainder - (remainder % 2)) / 2)

  @paddingWidth.GET
  def _getPaddingWidth(self) -> int:
    """Returns the padding width. """
    if TYPE_CHECKING:
      assert isinstance(self.borderWidth, int)
    remainder = self.__total_width__ - self.borderWidth
    return int((remainder + (remainder % 2)) / 2)

  @cornerRadius.GET
  def _getCornerRadius(self) -> int:
    """Returns the corner radius. """
    return maybe(self.__corner_radius__, self.__fallback_radius__)

  @cornerRadius.SET
  def _setCornerRadius(self, value: int) -> None:
    """Sets the corner radius. """
    self.__corner_radius__ = value

  def _getBoxModel(self) -> BoxModel:
    """Returns a BoxModel instance based on the current configuration. """
    if TYPE_CHECKING:
      assert isinstance(self.marginWidth, int)
      assert isinstance(self.borderWidth, int)
      assert isinstance(self.paddingWidth, int)
      assert isinstance(self.cornerRadius, int)
      assert isinstance(self.fillColor, RGBA)
      assert isinstance(self.borderColor, RGBA)
    box = BoxModel()
    box.marginShape = Margin(self.marginWidth)
    box.borderShape = Margin(self.borderWidth)
    box.paddingShape = Margin(self.paddingWidth)
    box.cornerRadiusX = self.cornerRadius
    box.cornerRadiusY = self.cornerRadius
    box.marginColor = RGBA(0, 0, 0, 0, )
    box.borderColor = self.borderColor
    box.paddingColor = self.fillColor
    return box

  def __get__(self, instance: object, owner: type) -> Any:
    """Returns the BoxModel object for the instance or the descriptor
    itself if instance is None. """
    if instance is None:
      return self
    return self._getBoxModel()

  def __set_name__(self, owner: type, name: str) -> None:
    """Sets the name of the field. """
    self.__field_name__ = name
    self.__field_owner__ = owner

  @overload(RGBA, RGBA, int, int)
  def __init__(self, *args) -> None:
    self.fillColor = args[0]
    self.borderColor = args[1]
    self.borderWidth = args[2]
    self.cornerRadius = args[3]

  @overload()
  def __init__(self, ) -> None:
    pass

  def __str__(self, ) -> str:
    """Returns a string representation of the instance. """
    info = """%s object at field name: %s owned by: %s"""
    clsName = type(self).__name__
    fieldName = self.__field_name__
    ownerName = self.__field_owner__.__name__
    return info % (clsName, fieldName, ownerName)
