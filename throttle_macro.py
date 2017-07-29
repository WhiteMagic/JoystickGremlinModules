import gremlin


# Joystick decorator
t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)


# Macro executed when the activation zone is entered by the axis
start_macro = gremlin.macro.Macro()
start_macro.press("Left Shift")


# Macro executed when the activation zone is left by the axis
stop_macro = gremlin.macro.Macro()
stop_macro.release("Left Shift")


# Virtual button that handles running the correct macro at the
# appropriate time
macro_axis_button = gremlin.actions.AxisButton(0.8, 1.0)


# Function executing the start and stop macro as requested
def callback(value, event):
    if value.current:
        gremlin.macro.MacroManager().add_macro(start_macro, None, event)
    else:
        gremlin.macro.MacroManager().add_macro(stop_macro, None, event)


# Axis binding which forwards the value to a virtual axis and also has a
# macro that is executed when the throttle enters a specific region and
# executes another one upon leaving.
@t16000m.axis(4)
def throttle_macro(event, vjoy):
    vjoy[1].axis(4).value = event.value
    macro_axis_button.process(event.value, lambda x: callback(x, event))
