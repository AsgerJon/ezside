"""AboutPython provides a custom dialog for displaying information about
the current version of Python and conda. This includes links to relevant
websites. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from PySide6.QtCore import QMargins
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QDialog, QHBoxLayout, QWidget
from icecream import ic
from worktoy.desc import AttriBox
from worktoy.text import monoSpace

from ezside.tools import Align
from ezside.basewidgets import Label, Label
from moreworktoy import mambaVersion


class AboutPythonDialog(QDialog):
  """AboutPython provides a custom dialog for displaying information about
  the current version of Python and conda. This includes links to relevant
  websites. """

  baseLayout = AttriBox[QVBoxLayout]()
  horizontalLayout = AttriBox[QHBoxLayout]()
  horizontalWidget = AttriBox[QWidget]()
  headerLabel = AttriBox[Label]('Python and Conda')
  infoLabel = AttriBox[Label]('')

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, QWidget):
        QDialog.__init__(self, arg)
        break
    else:
      QDialog.__init__(self)
    self.headerLabel.paddings = 6, 2
    self.infoLabel.paddings = 6, 2

  def show(self) -> None:
    """Show the dialog. """
    self.setWindowTitle('About Python and Mamba')
    info = """Python %d.%d.%d and Conda %d.%d.%d"""
    major, minor, micro = sys.version_info[:3]
    pythonText = 'Python %d.%d.%d' % (major, minor, micro)
    condaText = 'Mamba %s' % mambaVersion()
    self.headerLabel.text = '%s and %s' % (pythonText, condaText)
    self.headerLabel.font.size = 24
    self.headerLabel.font.family = 'Montserrat'
    self.headerLabel.font.align = Align.CENTER
    self.infoLabel.font.size = 24
    self.infoLabel.font.family = 'Montserrat'
    self.infoLabel.font.align = Align.CENTER
    self.horizontalLayout.addWidget(self.headerLabel)
    self.horizontalWidget.setLayout(self.horizontalLayout)
    self.baseLayout.addWidget(self.horizontalWidget)
    self.infoLabel.text = monoSpace("""This instance of Python is running 
      in a virtual mamba environment!""")
    self.baseLayout.addWidget(self.infoLabel)
    self.setLayout(self.baseLayout)
    QDialog.show(self)
