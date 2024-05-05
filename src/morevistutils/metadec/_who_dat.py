"""WhoDat is a special subclass of Replace, which applies to classes
changing their string representation to the '__qualname__' attribute. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistutils.waitaminute import typeMsg

from morevistutils.metadec import Replace


class WhoDat(Replace):
  """WhoDat is a special subclass of Replace, which applies to classes
    changing their string representation to the '__qualname__' attribute. """

  def _getReplacementMethod(self) -> callable:
    """Getter-function for the replacement method overwritten to always
    return
    the '__qualname__' attribute. """

    def __str__(cls) -> str:
      """By applying this to the class itself, it achieves the same as
      implementing this change in the metaclass level. """
      qualName = getattr(cls, '__qualname__', None)
      if isinstance(qualName, str):
        return qualName
      qualName = getattr(cls, '__name__', None)
      if isinstance(qualName, str):
        return qualName
      return type.__str__(cls)

    return __str__

  def __call__(self, cls: type) -> type:
    """Performs a type check since only types are supported. """
    self._setAttributeName('__str__')
    self._setReplacementMethod(self._getReplacementMethod())
    if isinstance(cls, type):
      cls = Replace.__call__(self, cls)
      if isinstance(cls, type):
        return cls
      e = typeMsg('cls', cls, type)
      raise TypeError(e)
    e = typeMsg('cls', cls, type)
    raise TypeError(e)