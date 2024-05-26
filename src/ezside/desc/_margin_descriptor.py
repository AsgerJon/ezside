"""MarginDescriptor implements the descriptor protocol for the Margin
class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QMargins, QMarginsF, QRectF, QRect, QSizeF, QSize
from vistutils.waitaminute import typeMsg

from ezside.desc import SettingsDescriptor


def parseMargins(*args, **kwargs) -> QMargins:
  """Parse the Margin arguments."""
  left = kwargs.get('left', None)
  top = kwargs.get('top', None)
  right = kwargs.get('right', None)
  bottom = kwargs.get('bottom', None)
  if isinstance(left, int) and isinstance(top, int):
    if isinstance(right, int) and isinstance(bottom, int):
      return QMargins(left, top, right, bottom)
  for arg in args:
    if isinstance(arg, QMargins):
      return arg
    if isinstance(arg, QMarginsF):
      return arg.toMargins()
  intArgs = [arg for arg in args if isinstance(arg, int)]
  if len(intArgs) == 1:
    return QMargins(intArgs[0], intArgs[0], intArgs[0], intArgs[0])
  if len(intArgs) in [2, 3]:
    return QMargins(intArgs[0], intArgs[1], intArgs[0], intArgs[1])
  if len(intArgs) == 4:
    return QMargins(*intArgs[:4])


class Margins(SettingsDescriptor):
  """MarginDescriptor implements the descriptor protocol for the Margin
  class."""

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QMargins

  def create(self, instance: object, owner: type, **kwargs) -> QMargins:
    """Create the content."""
    margins = parseMargins(*self.getArgs(), **self.getKwargs())
    if margins is None:
      return QMargins(0, 0, 0, 0)
    if isinstance(margins, QMarginsF):
      return margins.toMargins()
    if isinstance(margins, QMargins):
      return margins
    e = typeMsg('margins', margins, QMargins)
    raise TypeError(e)

  def __set__(self, instance: object, value: Any) -> None:
    """Setter-function for margins"""
    if isinstance(value, QMarginsF):
      value = value.toMargins()
    if isinstance(value, QRectF, ):
      value = value.toRect()
    if isinstance(value, QRect):
      value = QMargins(value.left(),
                       value.top(),
                       value.right(),
                       value.bottom())
    if isinstance(value, QSizeF):
      value = value.toSize()
    if isinstance(value, QSize):
      value = QMargins(value.width(),
                       value.height(),
                       value.width(),
                       value.height())
    if isinstance(value, int):
      value = QMargins(value, value, value, value)
    if isinstance(value, (list, tuple)):
      if len(value) == 1:
        value = QMargins(value[0], value[0], value[0], value[0])
      if len(value) == 2:
        value = QMargins(value[0], value[1], value[0], value[1])
      if len(value) == 3:
        value = QMargins(value[0], value[1], value[2], value[1])
      if len(value) == 4:
        value = QMargins(*value[:4])
    if not isinstance(value, QMargins):
      e = typeMsg('value', value, QMargins)
    SettingsDescriptor.__set__(self, instance, value)
