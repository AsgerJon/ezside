"""LabelField provides a text label property for widgets by implementing
the descriptor protocol. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.base import BaseObject
from worktoy.desc import CoreDescriptor
from worktoy.text import typeMsg

from ezside.core import TextModel


class LabelField(CoreDescriptor):
  """LabelField provides a text label property for widgets by implementing
  the descriptor protocol."""

  __pos_args__ = None
  __key_args__ = None

  def __init__(self, *args, **kwargs) -> None:
    if args:
      self.__pos_args__ = args
    if kwargs:
      self.__key_args__ = kwargs

  def _getPosArgs(self, ) -> list:
    """Get the positional arguments."""
    if self.__pos_args__ is None:
      return []
    return [*self.__pos_args__, ]

  def _getKeyArgs(self, ) -> dict:
    """Get the keyword arguments."""
    if self.__key_args__ is None:
      return {}
    return {**self.__key_args__, }

  def _createTextModel(self, instance: object = None) -> TextModel:
    """Create the text model for the label field."""
    posArgs = self._getPosArgs()
    keyArgs = self._getKeyArgs()
    return TextModel(*posArgs, **keyArgs)

  def __get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Getter-function for the underlying TextModel object"""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    textModel = getattr(instance, pvtName, None)
    if textModel is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      textModel = self._createTextModel(instance)
      setattr(instance, pvtName, textModel)
      return self.__get__(instance, owner, _recursion=True)
    if isinstance(textModel, TextModel):
      return textModel
    e = typeMsg(pvtName, textModel, TextModel)
    raise TypeError(e)

  def __set__(self, instance: object, newValue: object) -> None:
    """Setter-function for the underlying TextModel object"""
    if isinstance(newValue, TextModel):
      pvtName = self._getPrivateName()
      return setattr(instance, pvtName, newValue)
    if isinstance(newValue, str):
      owner = self.getFieldOwner()
      textModel = self.__get__(instance, owner)
      textModel.text = newValue
      return
    e = typeMsg('newValue', newValue, TextModel)
    raise TypeError(e)
