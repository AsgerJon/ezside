"""AppSettings subclasses the QSettings class and implements the following
customized functionality:

  - When receiving an unrecognized key, the AppSettings immediately raises
MissingSettingsError. The class forces the use of IniFormat and user
scope. Further, it requires that the running application defines both a
name and an organization name.

"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QSettings, QObject, QMargins, QPoint
from PySide6.QtGui import QIcon, QKeySequence, QFontDatabase
from attribox import AttriBox
from icecream import ic
from vistutils.waitaminute import typeMsg

from ezside.app import AppDesc, MissingSettingsError
from ezside.desc import emptyBrush, \
  SolidFill, \
  SolidLine, \
  Normal, \
  Bold, \
  parseFont, parseBrush, parsePen, Black, Red, Yellow

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class AppSettings(QSettings):
  """AppSettings subclasses the QSettings class and implements the following
  customized functionality:

  - When receiving an unrecognized key, the AppSettings immediately raises
  MissingSettingsError. The class forces the use of IniFormat and user
  scope. Further, it requires that the running application defines both a
  name and an organization name. """

  __instance_object__ = None

  app = AppDesc()
  __app_name__ = AttriBox[str]('')
  __org_name__ = AttriBox[str]('')

  def __init__(self, instance: QObject, *args, **kwargs) -> None:
    """Initializes the AppSettings."""
    format_ = QSettings.Format.IniFormat
    scope = QSettings.Scope.UserScope
    appName = self.app.applicationName()
    orgName = self.app.organizationName()
    if isinstance(instance, QObject):
      QSettings.__init__(self, format_, scope, orgName, appName, instance)
      self.__app_name__ = appName
      self.__org_name__ = orgName
      self.__instance_object__ = instance
    else:
      e = typeMsg('instance', instance, QObject)
      raise TypeError(e)

    self.setValue('geometry/margins', QMargins(2, 2, 2, 2, ))
    self.setValue('geometry/borders', QMargins(2, 2, 2, 2, ))
    self.setValue('geometry/paddings', QMargins(2, 2, 2, 2, ))
    self.setValue('geometry/radius', QPoint(2, 2, ))
    self.setValue('brush/margins', emptyBrush())
    self.setValue('brush/borders', parseBrush(Black, SolidFill))
    self.setValue('brush/paddings', emptyBrush())
    self.setValue('info/textFont', parsePen(Yellow, 1, SolidLine, ))
    self.setValue('warning/textFont', parsePen(Red, 1, SolidLine, ))
    self.setValue('normal/textFont', parsePen(Black, 1, SolidLine, ))
    self.setValue('header/textFont', parsePen(Black, 1, SolidLine, ))
    self.setValue('title/textFont', parsePen(Black, 1, SolidLine, ))
    self.setValue('info/font', parseFont('Courier', 12, Normal))
    self.setValue('warning/font', parseFont('Courier', 12, Normal))
    self.setValue('normal/font', parseFont('Montserrat', 12, Normal))
    self.setValue('header/font', parseFont('Montserrat', 16, Normal))
    self.setValue('title/font', parseFont('Montserrat', 20, Bold))

  def _getPath(self) -> str:
    """Getter-function for the path to the directory containing the settings
    file. """
    return os.path.dirname(QSettings.fileName(self, ))

  def _specialValue(self, key: str, ) -> Any:
    """This method provides special values for certain keys such as icons
    and shortcuts. """
    if 'icon/' in key:
      name = key.split('/')[-1]
      if name == 'debug':
        name = 'risitas'
      fileName = '%s.png' % name
      filePath = os.path.join(self.app.iconDir, fileName)
      if os.path.exists(filePath):
        if os.path.isfile(filePath):
          return QIcon(filePath)
      return self._specialValue('icon/risitas')
    if 'shortcut/' in key:
      if 'debug' in key:
        return QKeySequence.fromString('F%s' % key[-1])
      name = key.split('/')[-1]
      filePath = os.path.join(self.app.appDir, 'shortcuts.json')
      if os.path.exists(filePath):
        if os.path.isfile(filePath):
          with open(filePath, 'r') as file:
            data = json.load(file)
            textShortCut = data.get(name, None)
            return QKeySequence.fromString(textShortCut or '')
      return self.app.shortcut(name)

  def value(self, key: str, *args, **kwargs) -> Any:
    """Returns the value of the key. If the key is not recognized, the
    function raises MissingSettingsError. """
    special = self._specialValue(key)
    if special is not None:
      return special
    out = QSettings.value(self, key, None)
    if out is None:
      raise MissingSettingsError(key)

  def setValue(self, key: str, value: Any, *args, **kwargs) -> None:
    """Sets the value of the key. """
    QSettings.setValue(self, key, value)
    testValue = QSettings.value(self, key)

  def __str__(self, ) -> str:
    """Return a string representation of the AppSettings. """
    out = '%s - %s (settings)' % (self.__app_name__, self.__org_name__)

  def __repr__(self, ) -> str:
    """Return a string representation of the AppSettings. """
    insName = str(self.__instance_object__)
    return '%s(%s)' % (self.__class__.__name__, insName)
