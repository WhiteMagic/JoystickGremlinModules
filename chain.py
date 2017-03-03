import math
import time

import gremlin

t16000 = gremlin.input_devices.JoystickDecorator(
    "T.16000M",
    72331530,
    "Default"
)


class Chain:

    """Implements a simple chain class."""

    def __init__(self):
        """Creates a new instance."""
        self._actions = []
        self._current_index = 0

    def add_action(self, action):
        """Adds a new action to the chain sequence.

        :param action the action to append to the end of the chain sequence
        """
        self._actions.append(action)

    def __call__(self):
        """Runs the next action in the sequence, looping around if needed."""
        self._actions[self._current_index]()
        self._current_index = (self._current_index + 1) % len(self._actions)


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


# Create a chain with three actions
chain_1 = Chain()
chain_1.add_action(MacroAction(["1"]))
chain_1.add_action(MacroAction(["2"]))
chain_1.add_action(MacroAction([("LShift", "press"), "A", ("LShift", "release"), "B", "C"]))

# Create a chain with four actions
chain_2 = Chain()
chain_2.add_action(MacroAction([("LShift", "press")]))
chain_2.add_action(MacroAction(["Q", "H"]))
chain_2.add_action(MacroAction([("LShift", "release")]))
chain_2.add_action(MacroAction(["1", "H"]))


@t16000.button(1)
def trigger(event):
    if event.is_pressed:
        chain_1()


@t16000.button(2)
def secondary(event):
    if event.is_pressed:
        chain_2()
