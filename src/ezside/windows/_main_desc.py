"""Main provides the MainWindow class through the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from ezside.app import EZDesc
from ezside.desc import parseWindow

ic.configureOutput(includeContext=True)


class Main(EZDesc):
  """Main provides the MainWindow class through the descriptor protocol."""

  __main_window_class__ = None

  def __init__(self, *args, **kwargs) -> None:
    EZDesc.__init__(self, *args, **kwargs, id='mainWindow')
    self.__main_window_class__, args, kwargs = parseWindow(*args, **kwargs)

  def getContentClass(self) -> type:
    """Returns the content class."""
    return self.__main_window_class__

  def create(self, instance: type, owner: type, **kwargs) -> type:
    """Create the content."""
    mainWindowClass = self.getContentClass()
    mainWindow = mainWindowClass(id=self.__settings_id__)
    return mainWindow
