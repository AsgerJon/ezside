"""ControlData provides a class for storing data related to the control of
mouse and cursor aware widgets. In particular related to timings. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import BaseObject


class ControlData(BaseObject):
  """ControlData provides a class for storing data related to the control of
  mouse and cursor aware widgets. In particular related to timings. """

  #  If the mouse button is pressed for longer than the times given below,
  #  the potential click events are cancelled. The press-position stores
  #  the mouse position when the mouse button is pressed. If a move event
  #  registers a position more than the clickDrift value away from the
  #  press-position, before the mouse button is released, the click event
  #  cancels.
  singleClick = 300
  doubleClick = 300
  tripleClick = 300
  clickDrift = 5

  #  After releasing the mouse button, the associated click event is held
  #  to allow for double and triple clicks. On timeout, the click event is
  #  allowed to trigger. When releasing mouse button, the release-position
  #  is set and if a mouse move event later registers a position more than
  #  the multiClickDrift value away from the release-position, the click
  #  event emits immediately. Thus, if the user clicks a button and
  #  immediately moves away, this cancels the potential multi click and
  #  causes and immediate click event.
  singleDelay = 150
  doubleDelay = 150
  tripleDelay = 150  # Not used, triple-click triggers immediately
  multiClickDrift = 5

  #  If the mouse button is pressed for longer than the times given below,
  #  the relevant pressHold event triggers. Double and triple press-hold
  #  events are double and triple clicks where the last mouse press was
  #  held long enough.
  singleHold = 600
  doubleHold = 600
  tripleHold = 600

  #  Rest speed is the magnitude of the mouse velocity vector when the mouse
  #  is considered to be at rest. When a mouse move event receives an
  #  event that is determined to be resting, the start-rest position is
  #  set and the rest-delay timer is registered. If on timeout, the mouse
  #  are nearer to the start-rest position than the rest-radius limit,
  #  the cursor focus event triggers.
  restSpeed = 100
  restRadius = 5
  restDelay = 150
