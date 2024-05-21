"""DoubleSlider provides a widget with a slider, a title header,
and a value footer showing the current value of the slider. The widget
makes use of the HorizontalSlider and VerticalSlider widgets, which emit
values in unit range. The DoubleSlider introduces abstractions to scale
the signal to a user-defined range. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLayout
from attribox import AttriBox
from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from ezside.core import ORIENTATION, \
  HORIZONTAL, \
  VERTICAL, \
  Tight, \
  Orientation, \
  parseOrientation, Alignment, AlignVCenter, AlignHCenter, parseAlignment
from ezside.widgets import CanvasWidget, \
  Label, \
  VerticalSlider, \
  HorizontalSlider


class DoubleSlider(CanvasWidget):
  """DoubleSlider provides a widget with a slider, a title header,
  and a value footer showing the current value of the slider. The widget
  makes use of the HorizontalSlider and VerticalSlider widgets, which emit
  values in unit range. The DoubleSlider introduces abstractions to scale
  the signal to a user-defined range. """

  __fallback_orientation__ = HORIZONTAL
  __vertical_fallback_alignment__ = AlignVCenter
  __horizontal_fallback_alignment__ = AlignHCenter

  header = AttriBox[Label]('Slider', id='header')
  footer = AttriBox[Label]('0.0', id='header')
  verticalSlider = AttriBox[VerticalSlider]()
  horizontalSlider = AttriBox[HorizontalSlider]()
  verticalLayout = AttriBox[QVBoxLayout]()
  horizontalLayout = AttriBox[QHBoxLayout]()
  orientation = Orientation(HORIZONTAL)
  alignment = Alignment()
  minVal = AttriBox[float](0.0)
  maxVal = AttriBox[float](1.0)

  valueChanged = Signal(float)
  sliderReleased = Signal()
  sliderGrabbed = Signal()

  @staticmethod
  def _parseRanges(*args, **kwargs) -> tuple[float, float]:
    """Parses arguments to min and max values."""
    minKeys = stringList("""min, minVal, low, start""")
    maxKeys = stringList("""max, maxVal, high, end""")
    floatArgs = [float(i) for i in args if isinstance(i, (float, int))]
    minKwarg, maxKwarg = None, None
    minArg, maxArg = [*floatArgs, None, None][:2]
    for key in minKeys:
      if key in kwargs:
        minKwarg = kwargs[key]
        break
    for key in maxKeys:
      if key in kwargs:
        maxKwarg = kwargs[key]
        break
    return maybe(minArg, minKwarg, 0.0), maybe(maxArg, maxKwarg, 1.0)

  @staticmethod
  def _parseStrings(*args, **kwargs) -> tuple[str, str]:
    """Parses arguments to the title and to format specification strings."""
    strArgs = [*[i for i in args if isinstance(i, str)], None, None][:2]
    titleArg, fmtSpecArg = strArgs
    titleKeys = stringList("""title, header, name""")
    fmtSpecKeys = stringList("""format, fmt, spec, fmtSpec""")
    titleKwarg, fmtSpecKwarg = None, None
    for key in titleKeys:
      if key in kwargs:
        titleKwarg = kwargs[key]
        break
    for key in fmtSpecKeys:
      if key in kwargs:
        fmtSpecKwarg = kwargs[key]
        break
    if titleKwarg is not None and fmtSpecKwarg is None:
      title = titleKwarg
      fmtSpec = '%.3f' if titleArg is None else titleArg
      if not isinstance(title, str):
        e = typeMsg('title', title, str)
        raise TypeError(e)
      if not isinstance(fmtSpec, str):
        e = typeMsg('fmtSpec', fmtSpec, str)
        raise TypeError(e)
    else:
      title = maybe(titleArg, titleKwarg, 'Slider')
      fmtSpec = maybe(fmtSpecArg, fmtSpecKwarg, '%.3f')
    return title, fmtSpec

  def __init__(self, *args, **kwargs) -> None:
    CanvasWidget.__init__(self)
    orientation = parseOrientation(*args, **kwargs)
    self.orientation = maybe(orientation, self.__fallback_orientation__)
    vFbAlign = self.__vertical_fallback_alignment__
    hFbAlign = self.__horizontal_fallback_alignment__
    fbAlign = vFbAlign if self.orientation is VERTICAL else hFbAlign
    alignment = parseAlignment(*args, **kwargs)
    self.alignment = maybe(alignment, fbAlign)
    self.minVal, self.maxVal = self._parseRanges(*args, **kwargs)
    self._title, self._fmtSpec = self._parseStrings(*args, **kwargs)

  def _getLayout(self) -> QLayout:
    """Getter-function for the layouts of the given orientation"""
    if self.orientation is HORIZONTAL:
      return self.horizontalLayout
    if self.orientation is VERTICAL:
      return self.verticalLayout
    e = """Unable to recognize orientation flag!"""
    raise RuntimeError(e)

  def _getSlider(self) -> HorizontalSlider:
    """Getter-function for the object used as slider. This depends on the
    orientation. The type hint to HorizontalSlider reflects the
    implementation detail that the VerticalSlider subclasses
    HorizontalSlider. """
    if self.orientation is HORIZONTAL:
      return self.horizontalSlider
    if self.orientation is VERTICAL:
      return self.verticalSlider
    e = """Unable to recognize orientation flag!"""
    raise RuntimeError(e)

  def initUi(self, ) -> None:
    """Initializes the user interface. """
    self._getLayout().setSpacing(1)
    self._getLayout().setContentsMargins(2, 2, 2, 2, )
    self.header.text = self._title
    self.header.setSizePolicy(Tight, Tight)
    self.header.initUi()
    self._getLayout().addWidget(self.header)
    self._getSlider().initUi()
    self._getLayout().addWidget(self._getSlider())
    iniVal = self._getSlider().sliderValue()
    scaleIniVal = (self.maxVal - self.minVal) * iniVal + self.minVal
    self.footer.text = self._fmtSpec % scaleIniVal
    self.footer.setSizePolicy(Tight, Tight)
    self.footer.initUi()
    self._getLayout().addWidget(self.footer)
    self.setLayout(self._getLayout())

  def initSignalSlot(self) -> None:
    """This function connects the signals and slots of the widget."""
    self._getSlider().positionChanged.connect(self.scaleValueChanged)
    self._getSlider().handleReleased.connect(self.sliderReleased)
    self._getSlider().handleCancelled.connect(self.sliderReleased)
    self._getSlider().handleGrabbed.connect(self.sliderGrabbed)

  @Slot(float)
  def scaleValueChanged(self, val: float) -> None:
    """Slot-function for the scaled value changed signal."""
    scaledValue = (self.maxVal - self.minVal) * val + self.minVal
    self.valueChanged.emit(scaledValue)
    self.footer.text = self._fmtSpec % scaledValue

  def value(self, ) -> float:
    """Returns the scaled value"""
    span = self.maxVal - self.minVal
    return self._getSlider().sliderValue() * span + self.minVal
