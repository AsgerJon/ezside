"""Menu provides a simplified menu implementation"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar
from attribox import AttriClass, AttriBox
from icecream import ic
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.app.menus.shortcuts import getShortcut
from morevistutils.casenames import Name, TitleCase, SnakeCase

if TYPE_CHECKING:
  from ezside.app.menus import MainMenuBar
ic.configureOutput(includeContext=True, )


class Menu(QMenu, AttriClass):
  """A class for managing menus in the application."""

  __menu_class__ = True
  __menu_bar__ = None
  __named_actions__ = None
  __action_dictionary__ = None

  name = AttriBox[Name]()

  def __init__(self, name: str, bar: QMenuBar, *args: str) -> None:
    """Initializes the menu."""
    title = (Name(name) @ TitleCase).strip()
    QMenu.__init__(self, title, bar)
    getNames = getattr(bar, 'get%sActions' % title, None)
    if getNames is None:
      e = """Expected owning instance of Menu to have a method named
      'get%sActions', but received: '%s' of type: '%s'"""
      insName = '%s' % bar
      clsName = bar.__class__.__name__
      raise AttributeError(e % (title, insName, clsName))
    self._setBar(bar)
    if TYPE_CHECKING:
      assert isinstance(bar, MainMenuBar)
    names = [*bar.getNamedMenuActions(title.lower()), *args]
    self._setNames(*names)
    self.initStyle()
    self.initUi()
    self.initSignalSlot()

  def _setNames(self, *args) -> None:
    """Setter-function for named actions."""
    if self.__named_actions__ is None:
      self.__named_actions__ = []
    for arg in args:
      if isinstance(arg, str):
        self.__named_actions__.append(arg)

  def _getNames(self) -> list[str]:
    """Getter-function for named actions."""
    return self.__named_actions__ or []

  def _setBar(self, bar: QMenuBar) -> None:
    """Setter-function for the owning menu bar"""
    if self.__menu_bar__ is not None:
      e = """This menu already has a main menubar: '%s', but received new 
      menubar: '%s'!"""
      existing = str(self.__menu_bar__)
      newBar = str(bar)
      raise AttributeError(monoSpace(e % (existing, newBar)))
    if getattr(bar, '__main_menu_bar__', None) is None:
      e = """Expected owning instance of Menu to have set the attribute
      '__main_menu_bar__', but received: '%s' of type: '%s'"""
      insName = '%s' % bar
      clsName = bar.__class__.__name__
      raise AttributeError(e % (insName, clsName))
    self.__menu_bar__ = bar

  def getBar(self) -> Any:  # MainMenuBar
    """Getter-function for the owning menu bar"""
    bar = self.__menu_bar__
    if bar is not None:
      if getattr(bar, '__main_menu_bar__', None) is not None:
        return bar
      e = """Expected owning instance of Menu to have set the attribute
      '__main_menu_bar__', but received: '%s' of type: '%s'"""
      insName = '%s' % bar
      clsName = bar.__class__.__name__
      raise AttributeError(e % (insName, clsName))
    e = """Menu instance: '%s' missing required menu attribute!"""
    raise AttributeError(monoSpace(e % str(self)))

  def getMain(self) -> Any:  # MainWindow
    """Getter-function for the main window"""
    bar = self.getBar()
    return bar.getMain()

  def getApp(self, ) -> Any:  # App
    """Getter-function for the running application"""
    mainWindow = self.getMain()
    app = mainWindow.getApp()
    return app

  def initStyle(self) -> None:
    """Initializes the style of the menu. It is optional for subclasses
    whether to implement this method. """

  def initUi(self, ) -> None:
    """Initializes the user interface for the menu."""
    self._buildActions()

  def initSignalSlot(self) -> None:
    """Initializes the signal slot for the menu. It is optional for
    subclasses whether to implement this method. """

  def _getActionDictionary(self, **kwargs) -> dict[str, Optional[QAction]]:
    """Returns a dictionary of actions with their names as keys."""
    if self.__action_dictionary__ is None:
      self.__action_dictionary__ = {name: None for name in self._getNames()}
    if isinstance(self.__action_dictionary__, dict):
      return self.__action_dictionary__

  def _buildActions(self, ) -> None:
    """Builds the actions for the menu."""
    for name in self._getNames():
      if name == '__separator__' or not name:
        QMenu.addSeparator(self)
      else:
        self.__action_dictionary__ = {
          **self._getActionDictionary(), name: self.addAction(name)}

  def addAction(self, name: str, *args, **kwargs) -> QAction:
    """Adds an action to the menu."""
    if not name:
      return QMenu.addSeparator(self)
    name = Name(name)
    icon = self.getApp().getIcon(name @ SnakeCase)
    title = name @ TitleCase
    bar = self.getBar()
    shortcut = getShortcut(name @ SnakeCase)
    action = QMenu.addAction(self, icon, title, )
    action.setShortcut(shortcut)
    return action

  def getAction(self, actionName: str) -> QAction:
    """Returns the action with the given name. """
    name = Name(actionName)
    actionDictionary = self._getActionDictionary()
    names = [actionName, *[name @ Case for Case in Name.getNameCases()]]
    for name in names:
      if name in actionDictionary:
        action = actionDictionary[name]
        if isinstance(action, QAction):
          return action
        e = typeMsg('action', action, QAction)
        raise TypeError(e)
    else:
      e = """Menu: '%s' has no action named: '%s'!"""
      raise AttributeError(monoSpace(e % (self.name, actionName)))

  def connectAction(self, actionName: str, callMeMaybe, **kwargs) -> None:
    """Connects the action with the given name to a slot."""
    action = self.getAction(actionName)
    if action is None:
      return
    if kwargs.get('hovered', False):
      action.hovered.connect(callMeMaybe)
    else:
      action.triggered.connect(callMeMaybe)
