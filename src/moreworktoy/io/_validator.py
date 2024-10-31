"""The functions 'validateFile' and 'validateDir' are used to validate
file and directory paths, respectively. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os


def _validateExistence(fid: str) -> None:
  """This function validates the existence of a file or directory. If it
  does not exist, a FileNotFoundError is raised. """
  if not os.path.exists(fid):
    e = """No file or directory found at: '%s'!""" % fid
    raise FileNotFoundError(e)


def validateFile(fid: str) -> None:
  """This function validates the existence of a file. If it does not
  exist, a FileNotFoundError is raised. """
  _validateExistence(fid)
  if not os.path.isfile(fid):
    e = """Found directory at: '%s' instead of file!""" % fid
    raise IsADirectoryError(e)


def validateDir(fid: str) -> None:
  """This function validates the existence of a directory. If it does not
  exist, a FileNotFoundError is raised. """
  _validateExistence(fid)
  if not os.path.isdir(fid):
    e = """Found file at: '%s' instead of directory!""" % fid
    raise NotADirectoryError(e)
