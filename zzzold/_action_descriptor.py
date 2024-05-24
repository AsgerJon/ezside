"""Action implements the descriptor protocol for QAction instances. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAction
from attribox import AttriBox
from vistutils.text import stringList

from ezside.app import EZDesc
from ezside.menus import CoreMenu

Menu = CoreMenu


class Action(EZDesc):
  """Action implements the descriptor protocol for QAction instances. """

  name = AttriBox[str]()
  title = AttriBox[str]()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the Action."""
    EZDesc.__init__(self, *args, **kwargs)
    nameTitle = parseNameTitle(*args, **kwargs, _except=self.__settings_id__)
    self.name = nameTitle.get('name', None)
    self.title = nameTitle.get('title', None)

  def getContentClass(self) -> type:
    """Returns the content class."""
    return QAction

  def create(self, instance: Menu, owner: type, **kwargs) -> QAction:
    """Creates the action."""
