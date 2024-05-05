"""Label provides the general class for widgets whose primary function is
to display text. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
from typing import TYPE_CHECKING
from attribox import AttriBox

from ezside.widgets import BaseWidget

if TYPE_CHECKING:
  BaseWidget.__init__.__annotations__ = {
    'self': 'BaseWidget'
  }


class Label(BaseWidget):
  """Label provides the   general class for widgets"""

  __fallback_text__ = 'Label'

  text = AttriBox[str]('')

  def __init__(self, *args, **kwargs) -> None:
    posArgs = []
    iniText = None
    for arg in args:
      if isinstance(arg, str) and iniText is None:
        iniText = arg
      else:
        posArgs.append(arg)
    self.text = self.__fallback_text__ if iniText is None else iniText

    BaseWidget.__init__(self, *posArgs, **kwargs)
