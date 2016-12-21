import gremlin

t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)

# Amount trim is changed with every step, each axis spans the range [-1, 1]
g_step_size = 0.05
# Current trim value applied to X and Y axis
g_trim_offset = [0, 0]
# Storage for the analog trim configuration
g_trim_analog_start = [0, 0]


def update_axis(vjoy, joy):
    """Updates the axis value based on the current physical position.

    Uses the current trim settings to position the virtual axis based on the
    physical axis position

    :param vjoy vjoy object providing access to the virtual joysticks
    :param joy joy object providing access to the physical joysticks
    """
    vjoy[1].axis(1).value = joy[1].axis(1).value + g_trim_offset[0]
    vjoy[1].axis(2).value = joy[1].axis(1).value + g_trim_offset[1]


@t16000m.hat(1)
def trim_digital(event, vjoy, joy):
    """Performs trimming using the hat to indicate the direction.

    :param event the hat event containing which direction it was pushed in
    :param vjoy vjoy proxy
    :param joy joy proxy
    """
    global g_trim_offset
    g_trim_offset[0] += g_step_size * event.value[0]
    g_trim_offset[1] += g_step_size * event.value[1]
    update_axis(vjoy, joy)


@t16000m.axis(1)
def x_axis(event, vjoy):
    """Remaps the physical X axis onto the virtual X axis, applying trim.

    :param event event containing the physical axis value
    :param vjoy vjoy proxy
    """
    vjoy[1].axis(1).value = event.value + g_trim_offset[0]


@t16000m.axis(2)
def y_axis(event, vjoy):
    """Remaps the physical Y axis onto the virtual Y axis, applying trim.

    :param event event containing the physical axis value
    :param vjoy vjoy proxy
    """
    vjoy[1].axis(2).value = event.value + g_trim_offset[1]


@t16000m.button(8)
def reset_trim(event, vjoy, joy):
    """Resets the trim settings to [0, 0], i.e. no trim.

    :param event event indicating whether or not the button is being pressed
    :param vjoy vjoy proxy
    :param joy joy proxy
    """
    if event.is_pressed:
        global g_trim_offset
        g_trim_offset = [0, 0]
        update_axis(vjoy, joy)


@t16000m.button(10)
def trim_analog(event, vjoy, joy):
    """Analog trimming sequence using the joystick input to define the trim value.

    This is working as follows:
    1. Move stick into the desired position which indicates the amount of
       trim needed
    2. Press and hold button
    3. Let the stick move back to center
    4. Let go of the button

    When the button is let go the difference between the position at which the
    button was initially pressed and then finally released is computed and
    stored as the trim value.

    :param event event indicating whether or not the button is being pressed
    :param vjoy vjoy proxy
    :param joy joy proxy
    """
    if event.is_pressed:
        global g_trim_analog_start
        g_trim_analog_start = [joy[1].axis(1).value, joy[1].axis(2).value]
    elif not event.is_pressed:
        global g_trim_offset
        g_trim_offset = [
            g_trim_analog_start[0] - joy[1].axis(1).value,
            g_trim_analog_start[1] - joy[1].axis(2).value,
        ]
        update_axis(vjoy, joy)
