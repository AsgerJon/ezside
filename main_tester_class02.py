"""LMAO"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import QSize
from worktoy.desc import AttriBox


class MainWindow(QMainWindow):
  """This subclass of QMainWindow provides the main application window. """

  baseWidget = AttriBox[QWidget]()
  layout = AttriBox[QVBoxLayout]()
  welcomeLabel = AttriBox[QLabel]()
  exitButton = AttriBox[QPushButton]()

  def initUi(self) -> None:
    """This method sets up the user interface"""
    self.setMinimumSize(QSize(480, 320))
    self.setWindowTitle("Welcome to WorkToy!")
    self.welcomeLabel.setText("""Welcome to WorkToy!""")
    self.exitButton.setText("Exit")
    self.layout.addWidget(self.welcomeLabel)
    self.layout.addWidget(self.exitButton)
    self.baseWidget.setLayout(self.layout)
    self.setCentralWidget(self.baseWidget)

  def initSignalSlot(self) -> None:
    """This method connects the signals and slots"""
    self.exitButton.clicked.connect(self.close)

  def show(self) -> None:
    """This reimplementation calls 'initUi' and 'initSignalSlot' before
    calling the parent implementation"""
    self.initUi()
    self.initSignalSlot()
    QMainWindow.show(self)


if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  window.show()
  sys.exit(app.exec())
