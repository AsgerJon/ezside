"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
from typing import Callable

from icecream import ic

from ezside.app import MainWindow, App
from ezside.style import RGB
from tester_class_02 import SomeClass, AnotherClass


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world', MainWindow, ]
  [print(x) for x in stuff]


def tester01() -> int:
  """Main Tester Script"""
  app = App(MainWindow)
  retCode = app.exec()
  for name in app.getMissingNames():
    print('--%s' % name)
  return retCode


def tester02() -> None:
  """Main Tester Script"""
  lime = RGB(144, 255, 0)
  print(lime)


def tester03() -> None:
  """Main Tester Script"""
  someObj = SomeClass()
  anotherObj = AnotherClass()
  print(anotherObj.urMom)
  print(object.__getattribute__(anotherObj, 'urMom'))


def main(callMeMaybe: Callable) -> None:
  """Main Tester Script"""
  tic = time.time()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = callMeMaybe()
  print(77 * '-')
  print('Return Code: %s' % retCode)
  print('Runtime: %.3f seconds' % (time.time() - tic))


if __name__ == '__main__':
  main(tester01)
