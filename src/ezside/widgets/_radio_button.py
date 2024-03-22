"""RadioButton provides a button that can be turned on by a mouse click,
but which require input from somewhere else to reactivate."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen

from ezside.widgets import BaseWidget


class RadioButton(BaseWidget):
  """AnimatedToggleButton provides a button that can be turned on by a
  mouse"""

  __current_state__ = False
