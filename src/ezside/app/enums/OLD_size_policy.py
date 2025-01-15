"""SizePolicy enumerates the possible combinations of horizontal and
vertical size policies for the QOL app."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PySide6.QtWidgets import QSizePolicy
from worktoy.desc import Field
from worktoy.keenum import auto

from . import AbstractEnum, BaseSizePolicy


class SizePolicy(AbstractEnum):
  """SizePolicy enumerates the possible combinations of horizontal and
  vertical size policies for the QOL app."""

  @classmethod
  def getQClass(cls) -> Any:
    """Returns the Qt version of this enumeration."""
    return QSizePolicy

  horizontal = Field()
  vertical = Field()
  Q = Field()

  MAX = auto(BaseSizePolicy.MAX, BaseSizePolicy.MAX)
  MAX_PREFER = auto(BaseSizePolicy.MAX, BaseSizePolicy.PREFER)
  MAX_EXPAND = auto(BaseSizePolicy.MAX, BaseSizePolicy.EXPAND)

  PREFER_MAX = auto(BaseSizePolicy.PREFER, BaseSizePolicy.MAX)
  PREFER = auto(BaseSizePolicy.PREFER, BaseSizePolicy.PREFER)
  PREFER_EXPAND = auto(BaseSizePolicy.PREFER, BaseSizePolicy.EXPAND)

  EXPAND_MAX = auto(BaseSizePolicy.EXPAND, BaseSizePolicy.MAX)
  EXPAND_PREFER = auto(BaseSizePolicy.EXPAND, BaseSizePolicy.PREFER)
  EXPAND = auto(BaseSizePolicy.EXPAND, BaseSizePolicy.EXPAND)

  @horizontal.GET
  def _getHorizontal(self) -> BaseSizePolicy:
    """Returns the horizontal size policy."""
    return self.value[0]

  @vertical.GET
  def _getVertical(self) -> BaseSizePolicy:
    """Returns the vertical size policy."""
    return self.value[1]

  @Q.GET
  def _getQVersion(self) -> Any:
    """Returns the Qt version of this enumeration."""
    if TYPE_CHECKING:
      assert isinstance(self.horizontal, BaseSizePolicy)
      assert isinstance(self.vertical, BaseSizePolicy)
      assert isinstance(self.horizontal.value, QSizePolicy.Policy)
      assert isinstance(self.vertical.value, QSizePolicy.Policy)
    policy = QSizePolicy()
    policy.setHorizontalPolicy(self.horizontal.value)
    policy.setVerticalPolicy(self.vertical.value)
    return policy
