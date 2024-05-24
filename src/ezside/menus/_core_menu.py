"""CoreMenu provides the menu entry point for menus inheriting from both
QMenu and EZObject. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from attribox import AttriBox
from vistutils.waitaminute import typeMsg

from ezside.app import EZObject, Settings
from ezside.desc import parseParent

ic.configureOutput(includeContext=True)


class CoreMenu(QMenu, EZObject):
  """CoreMenu provides the menu entry point for menus inheriting from both
  QMenu and EZObject. """

  title = AttriBox[str]()
  settings = Settings()

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the CoreMenu."""
    EZObject.__init__(self, *args, **kwargs)
    parent = parseParent(*args, **kwargs)
    QMenu.__init__(self, parent)
    titleKeys = ['title', 'name', 'menuTitle', 'menuName', 'menu']
    for key in titleKeys:
      if key in kwargs:
        val = kwargs[key]
        if isinstance(val, str):
          self.title = val
          break
        e = typeMsg('title', val, str)
        raise TypeError(e)
    else:
      for arg in args:
        if isinstance(arg, str) and arg != self.__settings_id__:
          self.title = arg
          break
      else:
        e = """Menu instances must be initialized with a title!"""
        raise ValueError(e)

  def addAction(self, title: str, *args) -> QAction:
    """Add an action to the menu."""
    snakeName = title.lower().replace(' ', '_')
    name = title.replace(' ', '')
    camelName = '%s%s' % (name[0].lower(), name[1:])
    icon = self.settings.value('icon/%s' % snakeName, None)
    shortcut = self.settings.value('shortcut/%s' % camelName, None)
    action = QMenu.addAction(self, icon, title, shortcut)
    setattr(self.app.main, camelName, action)
    ic(camelName)
    return action

  def initUi(self, ) -> None:
    """Initializes the user interface."""
