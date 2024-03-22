"""The 'widgets' package provides the widgets for the main application
window. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._timer import Timer
from ._data_roll import DataRoll
from ._data_series import DataSeries, LineSeries, ScatterSeries
from ._base_widget import BaseWidget
from ._spacer import VSpacer, HSpacer, Spacer, AbstractSpacer
from ._control_widget import HorizontalAbstractControl, AbstractControl
from ._control_widget import VerticalAbstractControl, PushButton
from ._text_label import TextLabel
from ._spinbox import SpinBox
from ._data_view import DataView
from ._control_widget import AbstractControl, PushButton
from ._plot_envelope import PlotEnvelope
from ._filled_rect import FilledRect
from ._vertical_panel import VerticalPanel
from ._horizontal_panel import HorizontalPanel
from ._corner_panel import CornerPanel
from ._client_info import ClientInfo
from ._vertical_slider import VerticalSlider
from ._equalizer import Equalizer
from ._white_noise import WhiteNoise
from ._data_widget import DataWidget
