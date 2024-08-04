"""AbstractMenu provides an abstract base class for the menu classes.
Since metaclass conflicts prevent implementing the 'BaseObject' class as a
base class for the menu classes, a separate parser class which does
inherit from 'BaseObject' is used to collect values from arguments. This
parser implement function overloading. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never, Self

from PySide6.QtWidgets import QWidget, QMenu
from icecream import ic
from worktoy.desc import Field
from worktoy.meta import BaseObject, overload
from worktoy.parse import maybe
from worktoy.text import monoSpace, typeMsg

from ezside.app import EZAction
from ezside.parser import MenuParser

ic.configureOutput(includeContext=True)


class AbstractMenu(QMenu):
  """AbstractMenu provides an abstract base class for the menu classes.
  Since metaclass conflicts prevent implementing the 'BaseObject' class as a
  base class for the menu classes, a separate parser class which does
  inherit from 'BaseObject' is used to collect values from arguments. This
  parser implement function overloading. """

  __is_initialized__ = None

  __action_list__ = None
  __iter_contents__ = None
  __parsed_args__ = None

  parsed = Field()

  @parsed.SET
  def _setParsed(self, parsedObject: MenuParser) -> None:
    """Setter-function for the parsed."""
    self.__parsed_args__ = parsedObject

  @parsed.GET
  def _getParsed(self) -> MenuParser:
    """Getter-function for the parsed."""
    return self.__parsed_args__

  def __iter__(self, ) -> Self:
    """Implements the iteration protocol"""
    self.__iter_contents__ = [*maybe(self.__action_list__, [])]
    return self

  def __next__(self, ) -> EZAction:
    """Implements the iteration protocol"""
    if self.__iter_contents__:
      return self.__iter_contents__.pop(0)
    raise StopIteration

  def __getitem__(self, actionName: str) -> EZAction:
    """Allows action retrieval by name. """
    for ezAction in maybe(self.__action_list__, []):
      if actionName == str(ezAction):
        return ezAction
    e = """Unable to recognize action named: '%s' for menu: '%s'!"""
    raise KeyError(monoSpace(e % (actionName, self.parsed.title)))

  def __init__(self, *args) -> None:
    if len(args) > 2:
      e = """AbstractMenu parses at most 2 positional arguments, 
      but received: %d!""" % len(args)
      raise TypeError(monoSpace(e))
    someArgs = [arg for arg in args if arg is not None]
    self.parsed = MenuParser(*someArgs)
    QMenu.__init__(self, self.parsed.parent)
    self.setTitle(self.parsed.title)

  def __str__(self) -> str:
    return self.parsed.title

  def initUi(self) -> None:
    """Subclasses must implement this method to add actions to the menu."""

  def addAction(self, ezAction: EZAction, ) -> None:
    """The menus support only instances of the 'EZAction'. When adding
    them to the menu, they are stored in the menu instance and are
    available for iteration."""
    if not isinstance(ezAction, EZAction):
      e = typeMsg('ezAction', ezAction, EZAction)
      raise TypeError(e)
    actions = maybe(self.__action_list__, [])
    self.__action_list__ = [*actions, ezAction]
    return QMenu.addAction(self, ezAction)
