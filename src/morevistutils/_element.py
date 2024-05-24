"""Base class to seamlessly absorb initialization and subclassing
parameters."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class Element(object):
  """Base class to seamlessly absorb initialization and subclassing
  parameters.
    +------------------------------------------------+
    | This in-between class should not be necessary! |
    +------------------------------------------------+"""

  def __init__(self, *args, **kwargs) -> None:
    """Initialize without forwarding arguments to avoid object.__init__
    errors.
    +------------------------+
    | Why are we still here? |
    +------------------------+"""
    super().__init__()

  def __init_subclass__(cls, **kwargs) -> None:
    """Handles any subclass initialization parameters safely and quietly.
    +------------------------+
    | Just to suffer?        |
    +------------------------+"""
    super().__init_subclass__()
