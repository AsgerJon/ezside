"""The 'ezside.app.menus' package provides the menus for the main
application window."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._core_menu import CoreMenu
from ._file_menu import FileMenu, File
from ._edit_menu import EditMenu, Edit
from ._help_menu import HelpMenu, Help
from ._debug_menu import DebugMenu, Debug
from ._core_menu_bar import CoreMenuBar
from ._core_status_bar import CoreStatusBar
from ._menu_bar_desc import MenuBar
from ._status_bar_desc import StatusBar
