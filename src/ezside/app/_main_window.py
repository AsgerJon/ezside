"""This subclass should implement business logic."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from PySide6.QtCore import QMargins, QRectF, QPointF, QSizeF, QSize, Slot
from PySide6.QtGui import QColor, QFont, QFontDatabase, QResizeEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from icecream import ic
from pyperclip import copy

from ezside.app import LayoutWindow
from ezside.tools import SizeRule, MarginsBox

ic.configureOutput(includeContext=True)


class MainWindow(LayoutWindow):
  """This subclass should implement business logic."""
