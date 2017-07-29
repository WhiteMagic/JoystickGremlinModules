import math
import threading
import time

import gremlin

t16000 = gremlin.input_devices.JoystickDecorator(
    "T.16000M",
    72331530,
    "Default"
)


# Repeating macro with a single key
repeating_1 = gremlin.macro.Macro()
repeating_1.repeat = gremlin.macro.HoldRepeat(0.5)
repeating_1.tap("-")

# Repeating macro with three keys
repeating_2 = gremlin.macro.Macro()
repeating_2.repeat = gremlin.macro.HoldRepeat(1.0)
repeating_2.press("Left Shift")
repeating_2.tap("Q")
repeating_2.tap("H")
repeating_2.release("Left Shift")


@t16000.button(1)
def trigger(event):
    if event.is_pressed:
        gremlin.macro.MacroManager().add_macro(repeating_1, None, event)


@t16000.button(2)
def secondary(event):
    if event.is_pressed:
        gremlin.macro.MacroManager().add_macro(repeating_2, None, event)
