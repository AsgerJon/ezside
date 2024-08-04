"""FontFlag class provides a KeeNum enumeration of font flags."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from PySide6.QtGui import QFont
from worktoy.keenum import KeeNum, auto


class FontFlag(KeeNum):
  """FontFlag class provides a KeeNum enumeration of font flags."""

  @abstractmethod
  def apply(self, font: QFont) -> None:
    """Apply the font flag to the given QFont."""

  @abstractmethod
  def __bool__(self) -> bool:
    """Returns True if the font flag is set."""

  def __neg__(self) -> FontFlag:
    return self.LOW if self else self.HIGH


class Italic(FontFlag):
  """Italic flag for QFont."""

  HIGH = auto(True)
  LOW = auto(False)

  def apply(self, font: QFont) -> QFont:
    """Apply the font flag to the given QFont."""
    font.setItalic(True if self else False)
    return font

  def __bool__(self) -> bool:
    """Returns True if the font flag is set."""
    return True if self.value else False


class StrikeOut(FontFlag):
  """StrikeOut flag for QFont."""

  HIGH = auto(True)
  LOW = auto(False)

  def apply(self, font: QFont) -> QFont:
    """Apply the font flag to the given QFont."""
    font.setStrikeOut(True if self else False)
    return font

  def __bool__(self) -> bool:
    """Returns True if the font flag is set."""
    return True if self.value else False


class Underline(FontFlag):
  """Underline flag for QFont."""

  HIGH = auto(True)
  LOW = auto(False)

  def apply(self, font: QFont) -> QFont:
    """Apply the font flag to the given QFont."""
    font.setUnderline(True if self else False)
    return font

  def __bool__(self) -> bool:
    """Returns True if the font flag is set."""
    return True if self.value else False
