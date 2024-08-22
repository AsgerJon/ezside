"""AboutPython provides a custom dialog for displaying information about
the current version of Python and conda. This includes links to relevant
websites. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QVBoxLayout, QDialog, QHBoxLayout, QWidget
from worktoy.desc import AttriBox, THIS
from worktoy.text import monoSpace

from ezside.layouts import VerticalLayout
from ezside.tools import Align
from ezside.base_widgets import Label
from moreworktoy import mambaVersion


class AboutPythonDialog(QDialog):
  """AboutPython provides a custom dialog for displaying information about
  the current version of Python and conda. This includes links to relevant
  websites. """

  verticalLayout = AttriBox[VerticalLayout](THIS)
  headerLabel = AttriBox[Label]('Python and Conda', styleId='header')
  infoLabel = AttriBox[Label]('')

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QDialog.__init__(self, arg)
        break
    else:
      QDialog.__init__(self)
    self.setMinimumSize(320, 240)

  def show(self) -> None:
    """Show the dialog. """
    self.setWindowTitle('About Python and Mamba')
    info = """Python %d.%d.%d and Conda %d.%d.%d"""
    major, minor, micro = sys.version_info[:3]
    pythonText = 'Python %d.%d.%d' % (major, minor, micro)
    condaText = 'Mamba %s' % mambaVersion()
    self.headerLabel.text = '%s and %s' % (pythonText, condaText)
    self.infoLabel.text = monoSpace("""This instance of Python is running 
      in a virtual mamba environment!""")
    self.verticalLayout.addWidget(self.headerLabel)
    self.verticalLayout.addWidget(self.infoLabel)
    QDialog.show(self)
