"""App provides a subclass of QApplication. Please note that this subclass
provides only functionality relating to managing threads. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

MenuFlag = Qt.ApplicationAttribute.AA_DontUseNativeMenuBar


class App(QApplication):
  """App provides a subclass of QApplication. Please note that this subclass
  provides only functionality relating to managing threads. """

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
