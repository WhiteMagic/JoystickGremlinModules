import gremlin

# Joystick decorator
t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)

# Macro executed when the activation zone is entered by the axis
start_macro = gremlin.macro.Macro()
start_macro.action(gremlin.macro.Keys.LShift, True)

# Macro executed when the activation zon is left by the axis
stop_macro = gremlin.macro.Macro()
stop_macro.action(gremlin.macro.Keys.LShift, False)

# Virtual button that handles running the correct macro at the
# appropriate time
macro_axis_button = gremlin.util.AxisButton(0.8, 1.0)

# Function executing the start and stop macro as requested
def callback(is_pressed):
    if is_pressed:
        start_macro.run()
    else:
        stop_macro.run()

# Axis binding which forwards the value to a virtual axis and also has a
# macro that is executed when the throttle enters a specific region and
# executes another one upon leaving.
@t16000m.axis(4)
def throttle_macro(event, vjoy):
    vjoy[1].axis(4).value = event.value
    macro_axis_button.process(event.value, lambda x: callback(x))
