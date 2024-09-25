"""The 'getRoot' function returns the root of the project."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os


def _isRoot(directory: str) -> bool:
  """Tests if the given directory is the root of the project identfied by
  the presence of the '.root' file."""
  return True if '.root' in os.listdir(directory) else False


def _getParent(directory: str) -> str:
  """Returns the parent directory of the given directory."""
  parent = os.path.join(directory, '..')
  return os.path.normpath(os.path.abspath(parent))


def _getRoot(entry) -> str:
  """The '_getRoot' function starts at the given directory and recursively
  moves up the directory tree until it finds the root of the project. """
  if _isRoot(entry):
    return entry
  parent = _getParent(entry)
  if parent == entry:
    raise FileNotFoundError('Unable to find root of project!')
  return _getRoot(parent)


def getRoot() -> str:
  """The 'getRoot' function returns the root of the project."""
  entry = os.path.abspath(os.path.dirname(__file__))
  return _getRoot(entry)
