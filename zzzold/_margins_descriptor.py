"""Margins implements the descriptor protocol for instances of QMargins."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QMargins, QMarginsF
from attribox import AbstractDescriptor
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import parseMargins


class Margins(AbstractDescriptor):
  """The Margins class implements the descriptor protocol for QMargins. """

  __default_margins__ = None
  __fallback_margins__ = QMargins(0, 0, 0, 0, )

  def __init__(self, *args, **kwargs) -> None:
    margins = parseMargins(*args, **kwargs)
    if isinstance(margins, (QMargins, QMarginsF)):
      self.__default_margins__ = margins

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Implementation of the getter. The remaining functionality required
    by the descriptor protocol is implemented in the AbstractDescriptor
    class. """
    pvtName = self._getPrivateName()
    margins = getattr(instance, pvtName, None)
    if margins is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      margins = maybe(self.__default_margins__, self.__fallback_margins__)
      setattr(instance, pvtName, margins)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(margins, (QMargins, QMarginsF)):
      return margins
    e = typeMsg('margins', margins, QMarginsF, )
    raise TypeError(e)

  def __set__(self, instance: object, value: object) -> None:
    """Implementation of setter function. The AbstractDescriptor class
    requires subclasses implement this method explicitly for setting to be
    supported. While the descriptor protocol does not support the use of
    keyword arguments when setting values, any number of positional
    arguments may be given. If more than one is given, the received value
    argument becomes a tuple containing all of them. This descriptor
    supports setting to an existing instance of QMargins or QMarginsF or
    to positional arguments. In lieu of keyword arguments, dictionaries
    will be supported. """
    pvtName = self._getPrivateName()
    if isinstance(value, tuple):
      kwargs = {}
      args = []
      for arg in value:
        if isinstance(arg, dict):
          kwargs = {**kwargs, **arg}
        else:
          args.append(arg)
      margins = parseMargins(*args, **kwargs)
      if margins is None:
        e = """The setter function of the Margins instance was not able to 
        resolve the received value to a valid instance of QMargins or 
        QMarginsF!<br>Value received: %s""" % str(value)
        raise ValueError(monoSpace(e))
      if isinstance(margins, (QMarginsF, QMargins)):
        return self.__set__(instance, margins)
      e = typeMsg('margins', margins, QMargins)
      raise TypeError(e)
    if isinstance(value, list):
      return self.__set__(instance, tuple(*value, ))
    if isinstance(value, int):
      return self.__set__(instance, (value, value, value, value,))
    if isinstance(value, QMarginsF):
      return setattr(instance, pvtName, value.toMargins())
    if isinstance(value, QMargins):
      return setattr(instance, pvtName, value)
