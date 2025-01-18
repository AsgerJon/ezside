"""SizePolicy enumerates the possible combinations of horizontal and
vertical size policies for the QOL app."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PySide6.QtWidgets import QSizePolicy
from worktoy.base import BaseObject, overload
from worktoy.meta import BaseMetaclass
from worktoy.desc import Field
from worktoy.keenum import auto
from worktoy.parse import maybe
from worktoy.text import typeMsg

from . import AbstractEnum, BaseSizePolicy


class SizePolicy(BaseObject):
  """SizePolicy enumerates the possible combinations of horizontal and
  vertical size policies for the QOL app."""

  __fallback_horizontal__ = BaseSizePolicy.PREFER
  __fallback_vertical__ = BaseSizePolicy.PREFER

  __horizontal_policy__ = None
  __vertical_policy__ = None

  horizontal = Field()
  vertical = Field()
  Q = Field()

  @horizontal.GET
  def _getHorizontal(self) -> BaseSizePolicy:
    hPol = maybe(self.__horizontal_policy__, self.__fallback_horizontal__)
    if isinstance(hPol, BaseSizePolicy):
      return hPol
    e = typeMsg('__horizontal_policy__', hPol, BaseSizePolicy)
    raise TypeError(e)

  @horizontal.SET
  def _setHorizontal(self, value: Any, **kwargs) -> None:
    if isinstance(value, BaseSizePolicy):
      self.__horizontal_policy__ = value
    elif kwargs.get('_recursion', False):
      raise RecursionError
    else:
      try:
        policy = BaseSizePolicy(value)
        return self._setHorizontal(policy, _recursion=True)
      except Exception as exception:
        e = typeMsg('value', value, BaseSizePolicy)
        raise TypeError(e) from exception

  @vertical.GET
  def _getVertical(self) -> BaseSizePolicy:
    vPol = maybe(self.__vertical_policy__, self.__fallback_vertical__)
    if isinstance(vPol, BaseSizePolicy):
      return vPol
    e = typeMsg('__vertical_policy__', vPol, BaseSizePolicy)
    raise TypeError(e)

  @vertical.SET
  def _setVertical(self, value: Any, **kwargs) -> None:
    if isinstance(value, BaseSizePolicy):
      self.__vertical_policy__ = value
    elif kwargs.get('_recursion', False):
      raise RecursionError
    else:
      try:
        policy = BaseSizePolicy(value)
        return self._setVertical(policy, _recursion=True)
      except Exception as exception:
        e = typeMsg('value', value, BaseSizePolicy)
        raise TypeError(e) from exception

  @Q.GET
  def _getQVersion(self) -> QSizePolicy:
    """Returns the Qt version of this enumeration."""
    if TYPE_CHECKING:
      assert isinstance(self.horizontal, BaseSizePolicy)
      assert isinstance(self.vertical, BaseSizePolicy)
    policy = QSizePolicy()
    policy.setHorizontalPolicy(self.horizontal.Q)
    policy.setVerticalPolicy(self.vertical.Q)
    return policy
