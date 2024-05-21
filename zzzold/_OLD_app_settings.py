"""AppSettings subclasses the QSettings class."""
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from io import BytesIO
from mimetypes import guess_extension
import os
import sys
from typing import TYPE_CHECKING, Any, Union, Dict, Callable, Optional
from urllib.parse import urlparse

from PIL import Image
from PIL.Image import Resampling
from PySide6.QtCore import QSettings, QUrl, QCoreApplication
from PySide6.QtGui import QIcon, QKeySequence, QValidator, QImage
from attribox import AbstractDescriptor
from icecream import ic
import requests
from requests import RequestException
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from ezside.core import AlignHCenter, \
  AlignRight, \
  AlignLeft, \
  AlignCenter, \
  AlignFlag

if TYPE_CHECKING:
  from ezside.app import App, AppSettings

ic.configureOutput(includeContext=True, )

if sys.version_info.minor < 10:
  StrData = Union[Dict[str, str], str]
else:
  StrData = dict[str, str] | str


class _HTTPSValidator(QValidator):
  """Validates that strings are valid https urls."""

  __settings_instance__ = None

  def validate(self, url: str, *args, ) -> QValidator.State:
    """Validate the url."""
    parsedUrl = urlparse(url)
    if parsedUrl.scheme == 'https' and parsedUrl.netloc:
      return QValidator.State.Acceptable
    elif not url:
      return QValidator.State.Intermediate
    return QValidator.State.Invalid

  def __call__(self, url: str, ) -> bool:
    """Call the validator."""
    return self.validate(url, 69420) == QValidator.State.Acceptable

  def _getSettings(self) -> AppSettings:
    """Getter-function for the settings instance owning this validator."""
    if self.__settings_instance__ is None:
      app = QCoreApplication.instance()
      if TYPE_CHECKING:
        assert isinstance(app, App)
      settings = app.getSettings()
      if TYPE_CHECKING:
        assert isinstance(settings, AppSettings)
      return settings

  def getCachedFileName(self, url: str, ext: str = None) -> str:
    """Get the cached file name."""
    dirName = self._getSettings().getCachedDir()
    ext = 'NAN' if ext is None else ext
    fileName = '%s.%s' % (url.replace('/', '_').replace(':', '_'), ext)
    return os.path.join(dirName, fileName)

  def downloadImage(self, url: str, ) -> bool:
    """Download the url."""
    if self.validate(url) == QValidator.State.Acceptable:
      try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        try:
          img.verify()
        except Exception as exception:
          e = """When downloading image from url '%s' the content received 
          in the response failed to be verified by PIL by the following 
          exception: """ % url
          raise ValueError(monoSpace(e)) from exception
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')
        imgWidth, imgHeight = img.size
        aspect = imgWidth / imgHeight
        newWidth = imgWidth + 128
        newHeight = int(newWidth / aspect)
        img = img.resize((newWidth, newHeight), Resampling.LANCZOS)
        fid = self.getCachedFileName(url, 'png')
        img.save(fid, 'PNG')
        return True
      except RequestException as requestException:
        e = """When attempting to download the url: '%s', it was validated 
        as a valid https address, but when attempting to retrieve content, 
        the following exception was encountered:""" % url
        raise FileNotFoundError(monoSpace(e)) from requestException
    e = """The url: '%s' could not be validated as an https address!"""
    raise ValueError(monoSpace(e % url))


class _HTTPSValidatorDescriptor(AbstractDescriptor):
  """Implementation of descriptor protocol"""

  def __instance_get__(self, instance: object, owner: type, **kwargs) -> Any:
    """Implementation of the getter."""
    pvtName = self._getPrivateName()
    validator = getattr(instance, pvtName, None)
    if validator is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      validator = _HTTPSValidator()
      setattr(validator, '__settings_instance__', instance)
      setattr(instance, pvtName, validator)
      return self.__instance_get__(instance, owner, _recursion=True)
    if isinstance(validator, QValidator):
      return validator
    e = typeMsg('validator', validator, QValidator)
    raise TypeError(e)


class AppSettings(QSettings):
  """The 'AppSettings' class provides a convenient interface for
  working with the application's variable settings. """

  __on_missing__ = None
  __cached_directory__ = None

  browser = _HTTPSValidatorDescriptor()

  def setValue(self, key: str, value: Any) -> None:
    """Set the value of the key."""
    if isinstance(value, str):
      if self.browser(value):
        if self.group() == 'img' or key.split('/')[0] == 'img':
          self.browser.downloadImage(value)
          urlKey = '/'.join(['url', *key.split('/')[1:]])
          QSettings.setValue(self, urlKey, QUrl(value))
    return QSettings.setValue(self, key, value)

  @classmethod
  def _getShortcuts(cls, key: str = None) -> StrData:
    """Get the keyboard shortcuts."""
    if key is None:
      return {
        'new'      : 'CTRL+N',
        'open'     : 'CTRL+O',
        'save'     : 'CTRL+S',
        'saveAs'   : 'CTRL+SHIFT+S',
        'close'    : 'CTRL+W',
        'undo'     : 'CTRL+Z',
        'redo'     : 'CTRL+Y',
        'cut'      : 'CTRL+X',
        'copy'     : 'CTRL+C',
        'paste'    : 'CTRL+V',
        'selectAll': 'CTRL+A',
        'aboutQt'  : 'F12',
        'exit'     : 'ALT+F4',
        'debug1'   : 'F1',
        'debug2'   : 'F2',
        'debug3'   : 'F3',
        'debug4'   : 'F4',
        'debug5'   : 'F5',
        'debug6'   : 'F6',
        'debug7'   : 'F7',
        'debug8'   : 'F8',
        'debug9'   : 'F9',
        '__empty__': '',
      }
    if isinstance(key, str):
      shortcuts = cls._getShortcuts()
      if key in shortcuts:
        return shortcuts[key]
      return shortcuts['__empty__']
    e = typeMsg('key', key, str)
    raise TypeError(e)

  @classmethod
  def iconFolder(cls) -> str:
    """Returns the currently used icon folder"""
    here = os.path.dirname(__file__)
    there = os.path.join(here, 'iconfiles')
    return there

  @classmethod
  def _getIconPath(cls, key: str = None) -> StrData:
    """Get the icons."""
    if key is None:
      here = os.path.dirname(__file__)
      there = os.path.join(here, 'iconfiles')
      fileNames = {
        'editMenu'    : 'edit_menu',
        'add'         : 'add',
        'debug'       : 'debug',
        'exitImg'     : 'exit_img',
        'microphone'  : 'microphone',
        'aboutPython' : 'about_python',
        'cut'         : 'cut',
        'exit'        : 'exit',
        'unlocked'    : 'unlocked',
        'aboutQt'     : 'about_qt',
        'selectAll'   : 'select_all',
        'paste'       : 'paste',
        'redo'        : 'redo',
        'preferences' : 'preferences',
        'saveAs'      : 'save_as',
        'minescript'  : 'minescript',
        'screenShot'  : 'screen_shot',
        'undo'        : 'undo',
        'new'         : 'new',
        'risitas'     : 'risitas',
        'filesMenu'   : 'files_menu',
        'locked'      : 'locked',
        'aboutConda'  : 'about_conda',
        'files'       : 'files',
        'open'        : 'open',
        'save'        : 'save',
        'help'        : 'help',
        'copy'        : 'copy',
        'workside'    : 'workside',
        'aboutPySide6': 'about_py_side6',
        'aboutPySide' : 'about_py_side6',
        'helpMenu'    : 'help_menu',
        'pogchamp'    : 'pogchamp',
        '__empty__'   : 'risitas',
      }
      filePaths = {}
      for name, fileName in fileNames.items():
        filePath = os.path.join(there, '%s.png' % fileName)
        filePaths[name] = filePath
      return filePaths
    iconPaths = cls._getIconPath()
    if key in iconPaths:
      return iconPaths[key]
    return iconPaths['__empty__']

  @staticmethod
  def _parseInt(val: str) -> int | None:
    """Convert a string to an integer."""
    if all([c in '0123456789_' for c in val]):
      return int(val)
    return None

  @staticmethod
  def _parseFloat(val: str) -> float | None:
    """Convert a string to a float."""
    if all([c in '0123456789_.' for c in val]):
      if len(val) - len(val.replace('.', '')) > 1:
        return None
      return float(val)
    return None

  @staticmethod
  def _parseAlignment(val: str, key: str = None) -> int | None:
    """Parse the alignment."""
    if 'align' in key.lower():
      if 'horizontal' in key.lower():
        if 'center' in val.lower():
          return AlignHCenter
        if 'left' in val.lower():
          return AlignLeft
        if 'right' in val.lower():
          return AlignRight
      if 'vertical' in key.lower():
        if 'center' in val.lower():
          return AlignHCenter
        if 'top' in val.lower():
          return AlignLeft
        if 'bottom' in val.lower():
          return AlignRight
      if 'center' in val.lower():
        return AlignCenter
    return None

  def value(self, *args) -> Any:
    """Get the value of the key."""
    val = self._wrapValue(*args)
    key = args[0]
    if not isinstance(val, str):
      return val
    intVal = self._parseInt(val)
    if isinstance(intVal, int):
      return intVal
    floatVal = self._parseFloat(val)
    if isinstance(floatVal, float):
      return floatVal
    alignVal = self._parseAlignment(val, key)
    if isinstance(alignVal, AlignFlag):
      return alignVal

  def _wrapValue(self, *args) -> Any:
    """Get the value of the key."""
    key, fb, type_ = [*args, None, None, None][:3]
    if key is None:
      e = """At least a key must be provided!"""
      raise ValueError(monoSpace(e))
    keyWords = [w for w in key.split('/') if w]
    if keyWords[0] == 'icon':
      return QIcon(self._getIconPath(keyWords[1]))
    if keyWords[0] == 'shortcut':
      return QKeySequence(self._getShortcuts(keyWords[1]))
    if keyWords[0] == 'img':
      urlKey = '/'.join(['url', *keyWords[1:]])
      url = QSettings.value(self, urlKey)
      if isinstance(url, str):
        return self.loadImage(url)
    value = QSettings.value(self, key)
    if value is None:
      self._onMissing(key, fb)
      return fb
    if fb is None:
      return value
    if type_ is None:
      return QSettings.value(self, key, fb)
    return QSettings.value(self, key, fb, type_)

  def __init__(self, onMissing: Callable = None) -> None:
    """Initialize the AppSettings object."""
    QSettings.__init__(self, )
    if onMissing is not None:
      if callable(onMissing):
        self.__on_missing__ = onMissing
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    fid = QSettings.format(self)
    if isinstance(fid, str):
      if not os.path.isabs(fid):
        e = """Expected settings to use file location, but received: '%s'!"""
        raise OSError(e)
      cacheDir = os.path.join(fid, '.%s_cache' % os.path.basename(fid))
      if not os.path.exists(cacheDir):
        os.makedirs(cacheDir)
      if os.path.isdir(cacheDir):
        self.__cached_directory__ = cacheDir
      else:
        e = """Found a file at '%s', but expected a directory!"""
        raise IsADirectoryError(monoSpace(e % cacheDir))
      self.__cached_directory__ = cacheDir

  def getCachedDir(self, ) -> str:
    """Get the cached directory."""
    if self.__cached_directory__ is None:
      e = """The cache directory has not been set!"""
      raise FileNotFoundError(monoSpace(e))
    return self.__cached_directory__

  def loadImage(self, url: str, **kwargs) -> QImage:
    """Loads cached version or downloading and caching the image."""
    cachedImg = self.loadCachedImage(url)
    if cachedImg is not None:
      return cachedImg
    if kwargs.get('_recursion', False):
      raise RecursionError
    self.browser.downloadImage(url)
    return self.loadImage(url, _recursion=True)

  def loadCachedImage(self, url: str) -> Optional[QImage]:
    """Attempts to load the cached image."""
    fid = self.browser.getCachedFileName(url, 'png')
    if os.path.exists(fid):
      if os.path.isfile(fid):
        return QImage(fid)

  def _onMissing(self, key: str, fb: Any = None) -> Any:
    """Record missing value"""
    if self.__on_missing__ is None:
      return
    return self.__on_missing__(key, fb)

  def toStringFactory(self, cls: type) -> Callable:
    """Because QSettings is a scam pretending to save python objects,
    but instead saving text we here provide a factory for creating
    converters from the given type to a string. """
