"""The 'ezside.app' module provides application and main window classes. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._ez_action import EZAction
from ._abstract_menu import AbstractMenu
from ._file_menu import FileMenu
from ._edit_menu import EditMenu
from ._help_menu import HelpMenu
from ._debug_menu import DebugMenu
from ._menu_bar import MenuBar
from ._status_bar import StatusBar
from ._menu_window import MenuWindow
from ._base_window import BaseWindow
from ._layout_window import LayoutWindow
from ._main_window import MainWindow
from ._app import App
