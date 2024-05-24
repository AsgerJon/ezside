"""This file provides the entry point layouts."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout

from ezside.app import EZObject
from ezside.core import parseParent


class CoreVLayout(QVBoxLayout, EZObject):
  """CoreVLayout provides the entry point for vertical layouts inheriting
  from both QVBoxLayout and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreVLayout."""
    parent = parseParent(*args, **kwargs)
    QVBoxLayout.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)


class CoreHLayout(QHBoxLayout, EZObject):
  """CoreHLayout provides the entry point for horizontal layouts inheriting
  from both QVBoxLayout and EZObject. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreHLayout."""
    parent = parseParent(*args, **kwargs)
    QHBoxLayout.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)


class CoreGridLayout(QGridLayout, EZObject):
  """CoreGridLayout provides the entry point for grid layouts inheriting
  from QGridLayout. """

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreGridLayout."""
    parent = parseParent(*args, **kwargs)
    QGridLayout.__init__(self, parent)
    EZObject.__init__(self, *args, **kwargs)
