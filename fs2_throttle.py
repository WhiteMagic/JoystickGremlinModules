import math
import time

import gremlin

t16000 = gremlin.input_devices.JoystickDecorator(
    "T.16000M",
    72331530,
    "Default"
)

g_last_axis_value = 0.0

# Macros to send the throttle increase / decrease ccommands
increase = gremlin.input_devices.macro.Macro()
increase.tap("-")
decrease = gremlin.input_devices.macro.Macro()
decrease.tap("=")

@t16000.axis(4)
def fs2_throttle(event):
    """Sets the throttle to the desired value ensuring a consistent amount
    of key presses are sent, i.e. one per 5% of change in an axis.
    """
    global g_last_axis_value
    cur_value = event.value

    delta = cur_value - g_last_axis_value
    count = math.floor(abs(delta) / 0.05)
    action = increase if delta > 0 else decrease

    if count > 0:
        g_last_axis_value = cur_value

    for _ in range(count):
        action.run()
        time.sleep(0.025)



