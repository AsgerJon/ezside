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
from ezside.widgets import TextLabel
from moreworktoy import mambaVersion


class AboutPythonDialog(QDialog):
  """AboutPython provides a custom dialog for displaying information about
  the current version of Python and conda. This includes links to relevant
  websites. """

  baseLayout = AttriBox[QVBoxLayout]()
  horizontalLayout = AttriBox[QHBoxLayout]()
  horizontalWidget = AttriBox[QWidget]()
  headerLabel = AttriBox[TextLabel]('Python and Conda')
  left = AttriBox[TextLabel](' ')
  right = AttriBox[TextLabel](' ')
  infoLabel = AttriBox[TextLabel]('')

  def show(self) -> None:
    """Show the dialog. """
    ic(self.autoFillBackground())
    self.setWindowTitle('About Python and Mamba')
    info = """Python %d.%d.%d and Conda %d.%d.%d"""
    major, minor, micro = sys.version_info[:3]
    pythonText = 'Python %d.%d.%d' % (major, minor, micro)
    condaText = 'Mamba %s' % mambaVersion()
    self.headerLabel.text = '%s and %s' % (pythonText, condaText)
    self.headerLabel.fontSize = 24
    self.headerLabel.fontFamily = 'Montserrat'
    self.headerLabel.alignment = Align.CENTER
    self.left.text = '  '
    self.left.backgroundColor = QColor(255, 255, 255, 0, )
    self.right.backgroundColor = QColor(255, 255, 255, 0, )
    self.left.borderColor = QColor(255, 255, 255, 0, )
    self.right.borderColor = QColor(255, 255, 255, 0, )
    self.left.marginColor = QColor(255, 255, 255, 0, )
    self.right.marginColor = QColor(255, 255, 255, 0, )
    self.right.text = '  '
    self.horizontalLayout.addWidget(self.left)
    self.horizontalLayout.addWidget(self.headerLabel)
    self.horizontalLayout.addWidget(self.right)
    self.horizontalWidget.setLayout(self.horizontalLayout)
    self.baseLayout.addWidget(self.horizontalWidget)
    self.infoLabel.text = monoSpace("""This instance of Python is running 
      in a virtual mamba environment!""")
    self.baseLayout.addWidget(self.infoLabel)
    self.setLayout(self.baseLayout)
    QDialog.show(self)
