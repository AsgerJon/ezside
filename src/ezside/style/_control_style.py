"""ControlStyle provides settings for widgets implementing button presses.
The values provided here define values like the double click interval."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self, TypeAlias, Union
from worktoy.desc import AttriBox

from ezside.style import AbstractStyle

Data: TypeAlias = dict[str, Union[str, dict]]


class ControlStyle(AbstractStyle):
  """ControlStyle provides settings for widgets implementing button presses.
  The values provided here define values like the double click interval."""

  singleClick = AttriBox[int](300)
  doubleClick = AttriBox[int](300)
  tripleClick = AttriBox[int](300)
  clickDrift = AttriBox[int](5)

  singleDelay = AttriBox[int](150)
  doubleDelay = AttriBox[int](150)
  tripleDelay = AttriBox[int](150)
  multiClickDrift = AttriBox[int](5)

  singleHold = AttriBox[int](600)
  doubleHold = AttriBox[int](600)
  tripleHold = AttriBox[int](600)

  restSpeed = AttriBox[int](100)
  restRadius = AttriBox[int](5)
  restDelay = AttriBox[int](150)

  @classmethod
  def load(cls, data: Data) -> Self:
    """Loads the settings from the given data."""
    newControl = cls()
    newControl.singleClick = data.get('singleClick', 300)
    newControl.doubleClick = data.get('doubleClick', 300)
    newControl.tripleClick = data.get('tripleClick', 300)
    newControl.clickDrift = data.get('clickDrift', 5)

    newControl.singleDelay = data.get('singleDelay', 150)
    newControl.doubleDelay = data.get('doubleDelay', 150)
    newControl.tripleDelay = data.get('tripleDelay', 150)
    newControl.multiClickDrift = data.get('multiClickDrift', 5)

    newControl.singleHold = data.get('singleHold', 600)
    newControl.doubleHold = data.get('doubleHold', 600)
    newControl.tripleHold = data.get('tripleHold', 600)

    newControl.restSpeed = data.get('restSpeed', 100)
    newControl.restRadius = data.get('restRadius', 5)
    newControl.restDelay = data.get('restDelay', 150)

    return newControl

  def __str__(self) -> str:
    """Returns the string representation of the style."""
    out = ''
    for (key, value) in self.__class__.__dict__.items():
      out += f'{key}: {getattr(self, key)}\n'
    return out
