"""The 'mamba_info' module provides information about the mamba package."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os
import sys

from json import loads


def mambaVersion() -> str:
  """Return the version of the mamba package. """

  mini = os.path.join(sys.executable, '..', '..', '..', '..')
  mini = os.path.abspath(os.path.normpath(mini))
  mini = os.path.join(mini, 'conda-meta', )
  items = os.listdir(mini)
  for item in items:
    if 'libmambapy' in item:
      mini = os.path.normpath(os.path.join(mini, item))
      break
  else:
    raise FileNotFoundError
  with open(mini, 'r', encoding='utf-8') as file:
    data = file.read()
  data = loads(data)
  return data.get('version')
