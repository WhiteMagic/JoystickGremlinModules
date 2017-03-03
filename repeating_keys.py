import math
import threading
import time

import gremlin

t16000 = gremlin.input_devices.JoystickDecorator(
    "T.16000M",
    72331530,
    "Default"
)


class RepeatingMacro:

    """Repeteadly executes a macro."""

    def __init__(self, repeat_delay):
        """Creates a new repeating macro.

        ;param repeat_delay the time to wait before repeating the macro again
        """
        self._macros = []
        self._repeat_delay = repeat_delay
        self._timer = None

    def add_action(self, action):
        """Adds a MacroAction to this repeating macro.

        :param action the MacroAction instance to add
        """
        self._macros.append(action)

    def start(self):
        """Starts repeating the contained macros."""
        self._run_macros()

    def stop(self):
        """Stops repeating the contained macros."""
        if self._timer is not None:
            self._timer.cancel()

    def _run_macros(self):
        """Runs the macro and sets it up to run again after a delay."""
        for macro in self._macros:
            macro()
            time.sleep(0.025)
        self._timer = threading.Timer(self._repeat_delay, self._run_macros)
        self._timer.start()


class MacroAction:

    """Facilitates creating of macro sequences."""

    def __init__(self, keys):
        """Creates a new action macro.

        A single character indicates that a key should be tapped, if the key
        is a tuple consisting of (key, "release|press") the key will be either
        release or pressed.

        :param keys the inputs the macro should run
        """
        self._macro = gremlin.input_devices.macro.Macro()
        for key in keys:
            if isinstance(key, str):
                self._macro.tap(key)
            elif isinstance(key, tuple):
                if key[1] == "press":
                    self._macro.press(key[0])
                elif key[1] == "release":
                    self._macro.release(key[0])
            time.sleep(0.025)

    def __call__(self):
        """Executes the macro."""
        self._macro.run()


# Repeating macro with a single action
repeating_1 = RepeatingMacro(0.5)
repeating_1.add_action(MacroAction(["-"]))

# Repeating macro with two actions
repeating_2 = RepeatingMacro(1.0)
repeating_2.add_action(MacroAction([("LShift", "press")]))
repeating_2.add_action(MacroAction(["Q", "H"]))
repeating_2.add_action(MacroAction([("LShift", "release")]))


@t16000.button(1)
def trigger(event):
    if event.is_pressed:
        repeating_1.start()
    else:
        repeating_1.stop()


@t16000.button(2)
def secondary(event):
    if event.is_pressed:
        repeating_2.start()
    else:
        repeating_2.stop()
