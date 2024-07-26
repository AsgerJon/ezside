"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from types import ModuleType
import inspect

from PySide6.QtWidgets import QWidget
from worktoy.yolo import yolo

import ezside
from ezside.app import App, MainWindow


def tester01() -> int:
  """Main Tester Script"""
  return App(MainWindow).exec()


if __name__ == '__main__':
  yolo(tester01)
