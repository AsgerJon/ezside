"""Main Tester Script"""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys
import time
from typing import Callable

from ezside.app import App, MainWindow


def tester01() -> int:
  """Main Tester Script"""
  return App(MainWindow, ).exec()


def main(callMeMaybe: Callable) -> None:
  """Main Tester Script"""
  tic = time.time()
  print('Running python script located at: \n%s' % sys.argv[0])
  print('Started at: %s' % time.ctime())
  print(77 * '-')
  retCode = 0
  try:
    retCode = callMeMaybe()
  except Exception as exception:
    print('Exception: %s' % exception)
    raise exception
  retCode = 0 if retCode is None else retCode
  print(77 * '-')
  print('Return Code: %s' % retCode)
  print('Runtime: %.3f seconds' % (time.time() - tic))


if __name__ == '__main__':
  main(tester01)
