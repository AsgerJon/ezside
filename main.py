"""Main Tester Script"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from types import ModuleType
import inspect

from PySide6.QtWidgets import QWidget
from worktoy.yolo import yolo, stubGen

import ezside
from ezside.app import App, MainWindow


def tester01() -> int:
  """Main Tester Script"""
  return App(MainWindow, ).exec()


def tester02() -> int:
  """Rubbing stub generation"""

  for (key, val) in ezside.__dict__.items():
    if isinstance(val, ModuleType):
      for (key, val) in val.__dict__.items():
        if isinstance(val, ModuleType):
          for (key2, val2) in val.__dict__.items():
            if isinstance(val2, type(QWidget)):
              if 'ezside' in val2.__module__:
                stubGen(val2)
        if isinstance(val, type(QWidget)):
          if 'ezside' in val.__module__:
            stubGen(val)
  return 0


if __name__ == '__main__':
  yolo(tester02)
