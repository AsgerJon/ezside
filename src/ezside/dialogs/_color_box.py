"""ColorBox implements the descriptor protocol allowing owning instances
to access the default color, while also exposing a slot that when
triggered opens a color selection dialog. The 'accepted' signal of this
dialog is connected to the '__set__' method of the descriptor, allowing
user input to change the color at the given attribute name for the
relevant instance. Please note that all instances of the owning class will
have the same default color, but that the color selection dialog is
specific to the instance triggering it. Besides the dialog selection,
the descriptor class does implement the traditional setter method,
allowing constructors to set instance specific colors. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import TypedDescriptor


class ColorBox(TypedDescriptor):
  """ColorBox implements the descriptor protocol allowing owning instances
  to access the default color, while also exposing a slot that when
  triggered opens a color selection dialog. The 'accepted' signal of this
  dialog is connected to the '__set__' method of the descriptor, allowing
  user input to change the color at the given attribute name for the
  relevant instance. Please note that all instances of the owning class will
  have the same default color, but that the color selection dialog is
  specific to the instance triggering it. Besides the dialog selection,
  the descriptor class does implement the traditional setter method,
  allowing constructors to set instance specific colors. """
