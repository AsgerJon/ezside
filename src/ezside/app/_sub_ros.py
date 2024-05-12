#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
#
# import time
# from typing import Any, Callable
#
# from PySide6.QtCore import QThread, Signal
# from icecream import ic
# #  from msgs.msg import Float32Stamped
# from rospy import Subscriber, spin
# from vistutils.waitaminute import typeMsg
#
# from ezros.rosutils import resolveTopicType, initNodeMaybe
#
# ic.configureOutput(includeContext=True)
#
#
# class SubRos(QThread):
#   """RosThread instances represent a named topic and PySide6 signal. The
#   class provides an internal subscriber and callback function,
#   which implements a signal emission containing the message through the Qt
#   signal protocol. Thus, this class provides a bridge between the
#   publisher/subscriber system of ROS with the event-driven system of Qt."""
#
#   __topic_name__ = None
#   __topic_type__ = None
#   __ros_subscriber__ = None
#   __explicit_callback__ = None
#
#   data = Signal(complex)
#
#   def __init__(self, topicName: str, ) -> None:
#     """Initializes the RosThread instance."""
#     QThread.__init__(self)
#     self.__topic_name__ = topicName
#     self.__topic_type__ = resolveTopicType(self.__topic_name__)
#
#   def run(self) -> None:
#     """Runs the thread."""
#     initNodeMaybe()
#     self.__ros_subscriber__ = Subscriber(self.__topic_name__,
#                                          self.__topic_type__,
#                                          self._getCallback())
#     spin()
#
#   def _fallbackCallback(self, data: Float32Stamped) -> None:
#     """Callback function for the subscriber."""
#     self.data.emit(data)
#
#   def _setCallback(self, callMeMaybe: Callable) -> Callable:
#     """Setter-function for the callback."""
#     if self.__explicit_callback__ is not None:
#       e = 'The callback has already been set!'
#       raise AttributeError(e)
#     if callable(callMeMaybe):
#       self.__explicit_callback__ = callMeMaybe
#       return self.__explicit_callback__
#     e = typeMsg('callMeMaybe', callMeMaybe, Callable)
#     raise TypeError(e)
#
#   def _getCallback(self) -> Callable:
#     """Getter-function for the callback."""
#     if self.__explicit_callback__ is not None:
#       if callable(self.__explicit_callback__):
#         return self.__explicit_callback__
#       e = typeMsg('self.__explicit_callback__',
#                   self.__explicit_callback__,
#                   Callable)
#       raise TypeError(e)
#     return self._fallbackCallback
#
#   def __call__(self, callMeMaybe: Callable) -> Callable:
#     """Setter-function for the callback."""
#     return self._setCallback(callMeMaybe)
