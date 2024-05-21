"""SubClassError provides a special exception class for errors related to
subclasses. This exception should be raised when a call to 'issubclass'
provides the wrong result. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations


class SubClassError(TypeError):
  """SubClassError provides a special exception class for errors related to
  subclasses. This exception should be raised when a call to 'issubclass'
  provides the wrong result. """

  @staticmethod
  def _notSub() -> str:
    """Factory function creating the format spec for the message
    reflecting that the subclass is not a subclass, but was meant to."""
    return """Expected class: '%s' to be a subclass of '%s'!"""

  @staticmethod
  def _isSub() -> str:
    """Factory function creating the format spec for the message
    reflecting that the subclass is a subclass, but was not meant to."""
    return """Class '%s' cannot be a subclass of '%s'!"""

  @staticmethod
  def _msgFactory(bcls: type, scls: type) -> str:
    """Factory function creating error message. """
    if issubclass(scls, bcls):
      return SubClassError._isSub() % (scls, bcls)
    return SubClassError._notSub() % (scls, bcls)

  def __init__(self, cls, subCls, msg=None) -> None:
    """Initialize the exception."""
    if msg is None:
      msg = SubClassError._msgFactory(cls, subCls)
    super().__init__(msg)
