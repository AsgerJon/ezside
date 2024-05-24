"""The fontFamilies modules provides font family names. Please note, that
the list of font family names cannot be retrieved before the application
is running. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from icecream import ic

ic.configureOutput(includeContext=True)

here = os.path.dirname(os.path.abspath(__file__))
fileName = 'font_families.txt'
fid = os.path.join(here, fileName)
with open(fid, 'r') as f:
  FontFamilies = [item.strip() for item in f.readlines()]
