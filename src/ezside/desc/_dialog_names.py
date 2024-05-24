"""The 'dialogNames' module provides descriptor classes and parsers for
various core types in the PySide6 module."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QColorDialog, QFontDialog, QFileDialog

ColDialogOpt = QColorDialog.ColorDialogOption
showAlpha = QColorDialog.ColorDialogOption.ShowAlphaChannel
hideEye = QColorDialog.ColorDialogOption.NoEyeDropperButton
ColNotNative = QColorDialog.ColorDialogOption.DontUseNativeDialog

FontDialogOpt = QFontDialog.FontDialogOption
FontNotNative = QFontDialog.FontDialogOption.DontUseNativeDialog
ScaleFonts = QFontDialog.FontDialogOption.ScalableFonts
NotScaleFonts = QFontDialog.FontDialogOption.NonScalableFonts
MonoFonts = QFontDialog.FontDialogOption.MonospacedFonts
propFonts = QFontDialog.FontDialogOption.ProportionalFonts

FileOpt = QFileDialog.Option
FileShowDirs = QFileDialog.Option.ShowDirsOnly
FileNoConfirm = QFileDialog.Option.DontConfirmOverwrite

FileAccept = QFileDialog.AcceptMode
FileOpen = QFileDialog.AcceptMode.AcceptOpen
FileSave = QFileDialog.AcceptMode.AcceptSave

FileMode = QFileDialog.FileMode
FileAny = QFileDialog.FileMode.AnyFile
FileExit = QFileDialog.FileMode.ExistingFile
FileDir = QFileDialog.FileMode.Directory
FilesExit = QFileDialog.FileMode.ExistingFiles

FileView = QFileDialog.ViewMode
FileList = QFileDialog.ViewMode.List
FileDetail = QFileDialog.ViewMode.Detail

__all__ = [
  'ColDialogOpt', 'showAlpha', 'hideEye', 'ColNotNative',
  'FontDialogOpt', 'FontNotNative', 'ScaleFonts', 'NotScaleFonts',
  'MonoFonts', 'propFonts', 'FileOpt', 'FileShowDirs', 'FileNoConfirm',
  'FileAccept', 'FileOpen', 'FileSave', 'FileMode', 'FileAny', 'FileExit',
  'FileDir', 'FilesExit', 'FileView', 'FileList', 'FileDetail'
]
