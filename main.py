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


def tester00() -> None:
  """Main Tester Script"""
  stuff = [os, sys, ic, 'hello', 'world', MainWindow, ]
  [print(x) for x in stuff]


def tester01() -> int:
  """Main Tester Script"""
  return App().exec()


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
