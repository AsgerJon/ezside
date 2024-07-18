"""AUTO-GENERATED STUB FILE!"""
# AGPL-3.0 license
# Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ezside.app.menus import AbstractMenu
from ezside.app.menus import Action


class FileMenu(AbstractMenu):
  """FileMenu provides the file menu for the main application window. It
   subclasses the AbstractMenu class."""
  newAction: Action
  openAction: Action
  saveAction: Action
  saveAsAction: Action
  prefAction: Action
  exitAction: Action
