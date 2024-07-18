"""AUTO-GENERATED STUB FILE!"""
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QMenuBar
from ezside.app.menus import FileMenu
from ezside.app.menus import EditMenu
from ezside.app.menus import HelpMenu
from ezside.app.menus import DebugMenu


class MainMenuBar(QMenuBar):
  """MainMenuBar subclasses QMenuBar and brings common menus with common actions. """
  fileMenu: FileMenu
  editMenu: EditMenu
  helpMenu: HelpMenu
  debugMenu: DebugMenu