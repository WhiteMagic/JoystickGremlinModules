from PyQt5 import QtCore

import gremlin

# Joystick callback generation decorator
t16000 = gremlin.input_devices.JoystickDecorator(
    "T.16000M",
    72331530,
    "Default"
)


class OnReleaseExecutor(QtCore.QObject):

    """Runs specified callback on release of an input."""

    def __init__(self):
        """Creates a new instance."""
        super().__init__()

        self._registry = {}
        el = gremlin.event_handler.EventListener()
        el.joystick_event.connect(self._joystick_cb)

    def register(self, callback, physical_event):
        """Register a callback to run for a particular event.

        :param callback the function to run when the specified input is released
        :param physical_event the event describing the event on which to
            trigger
        """
        release_evt = physical_event.clone()
        release_evt.is_pressed = False

        if release_evt not in self._registry:
            self._registry[release_evt] = []
        self._registry[release_evt].append(callback)

    def _joystick_cb(self, evt):
        """Handles joystick events.

        :param evt the event to process
        """
        if evt in self._registry and not evt.is_pressed:
            for callback in self._registry[evt]:
                callback()
            self._registry[evt] = []


# Create callback executor instance
release_exec = OnReleaseExecutor()


def temporary_mode_switch(event, value, condition, mode):
    """Action allowing to temporarily switch to a mode and back.

    :param event the value of the physical event triggering the action
    :param value the input value
    :param condition activation condition for this action
    :param mode the mode to switch to
    """
    if value.current:
        release_exec.register(
            gremlin.control_action.switch_to_previous_mode,
            event
        )
        gremlin.control_action.switch_mode(mode)


# Action executed on the short press, mapping to the desired vJoy button
remap_action = gremlin.actions.Factory.remap_input(
        gremlin.common.InputType.JoystickButton,
        gremlin.common.InputType.JoystickButton,
        1,
        10
)


# Action executed on the long press, switching to the specified mode as long
# as the button is held down
mode_switch_action = lambda event, value, condition: temporary_mode_switch(
        event,
        value,
        condition,
        "Second"
)


# Tempo container, which holds both of the above actions and executes them
# based on the duration the button is being held down
tempo_mode_switch_container = gremlin.actions.Tempo(
        [
            remap_action,
            mode_switch_action
        ],
        None,
        0.5
)


@t16000.button(2)
def tempo_mode_switch(event):
    """Actual callback that triggers when the 2nd button is pressed."""
    value = gremlin.actions.Value(event.is_pressed)
    tempo_mode_switch_container(event, value)

