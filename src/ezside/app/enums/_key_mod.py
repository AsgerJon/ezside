"""CompoundModifier enumerates the possible states of the compound
modifier keys."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from enum import EnumType
from typing import TYPE_CHECKING, Any, Self

from PySide6.QtCore import Qt
from worktoy.keenum import auto, SpaceNum

from . import AbstractEnum

_Q_NO_MODIFIER = Qt.KeyboardModifier.NoModifier
_Q_SHIFT = Qt.KeyboardModifier.ShiftModifier
_Q_CTRL = Qt.KeyboardModifier.ControlModifier
_Q_ALT = Qt.KeyboardModifier.AltModifier
_Q_META = Qt.KeyboardModifier.MetaModifier


class KeyMod(AbstractEnum):
  """KeyMod enumerates the possible states of the modifier keys."""

  @classmethod
  def getQClass(cls) -> EnumType:
    """Returns the Qt version of this enumeration."""
    return Qt.KeyboardModifier

  NULL = auto(_Q_NO_MODIFIER)
  SHIFT = auto(_Q_SHIFT)
  CTRL = auto(_Q_CTRL)
  ALT = auto(_Q_ALT)
  META = auto(_Q_META)

  SHIFT_CTRL = auto(_Q_SHIFT | _Q_CTRL)
  SHIFT_ALT = auto(_Q_SHIFT | _Q_ALT)
  SHIFT_META = auto(_Q_SHIFT | _Q_META)

  CTRL_ALT = auto(_Q_CTRL | _Q_ALT)
  CTRL_META = auto(_Q_CTRL | _Q_META)

  ALT_META = auto(_Q_ALT | _Q_META)

  CTRL_ALT_META = auto(_Q_CTRL | _Q_ALT | _Q_META)  # No SHIFT
  SHIFT_ALT_META = auto(_Q_SHIFT | _Q_ALT | _Q_META)  # No CTRL
  SHIFT_CTRL_META = auto(_Q_SHIFT | _Q_CTRL | _Q_META)  # No ALT
  SHIFT_CTRL_ALT = auto(_Q_SHIFT | _Q_CTRL | _Q_ALT)  # No META

  SHIFT_CTRL_ALT_META = auto(_Q_SHIFT | _Q_CTRL | _Q_ALT | _Q_META)
  ALL = auto(_Q_SHIFT | _Q_CTRL | _Q_ALT | _Q_META)

  def __bool__(self) -> bool:
    return False if self.name == 'NULL' else True

  @classmethod
  def _getBaseNames(cls) -> list[str]:
    return ['SHIFT', 'CTRL', 'ALT', 'META']

  def components(self) -> list[Self]:
    cls = type(self)
    if not self:
      return []
    componentNames = self.name.split('_')
    out = []
    for name in componentNames:
      component = getattr(cls, name, None)
      if component is None:
        e = f"""Could not find component: '{name}'!"""
        raise AttributeError(e)
      out.append(component)
    return out

  def __getattr__(self, key: str, **kwargs) -> Any:
    try:
      return AbstractEnum.__getattr__(self, key)
    except AttributeError:
      keyNames = key.split('_')
      baseNames = self._getBaseNames()
      outNames = []
      for name in keyNames:
        if name not in baseNames:
          e = f"""Could not find base name: '{name}'!"""
          raise AttributeError(e)
        outNames.append(name)
      outName = '_'.join(outNames)
      cls = type(self)
      for member in cls:
        if member.name.lower() == outName.lower():
          return member
      return object.__getattribute__(self, key)

  def isBase(self, ) -> bool:
    if self:
      return True if self.name in self._getBaseNames() else False
    return False
