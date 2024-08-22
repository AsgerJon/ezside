"""NewDialog opens a dialog asking for a file name and for the dimensions
of the new image. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QDialog
from worktoy.desc import THIS, AttriBox, Field

from ezside.layouts import AbstractLayout
from ezside.base_widgets import Label


class NewDialog(QDialog):
  """NewDialog opens a dialog asking for a file name and for the dimensions
  of the new image. """

  __fallback_width__ = 256
  __fallback_height__ = 256
  __fallback_file_name__ = 'unnamed.png'

  width = Field()
  height = Field()
  fileName = Field()

  baseLayout = AttriBox[AbstractLayout](THIS)
  welcomeLabel = AttriBox[Label](THIS, 'Welcome to the new image dialog!')
