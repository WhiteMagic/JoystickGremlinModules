import gremlin


# Joystick callback generation decorator
t16000 = gremlin.input_devices.JoystickDecorator(
    "T.16000M",
    72331530,
    "Default"
)


# Windows ID of the physical device whose axis is used for the throttle
phys_device_id = 1
# Axis ID of the physical throttle
phys_throttle_id = 4
# Physical button used to toggle the cruise mode
phys_cruise_button = 2
# vJoy device ID to use
vjoy_device_id = 1
# vJoy axis ID to use
vjoy_throttle_id = 3
# vJoy button id mapped to the AB function in SC
vjoy_ab_button = 4
# Value to use when setting throttle to 100%, either -1 or 1
max_throttle_value = -1
# Flag indicating whether or not throttle commands should be applied
throttle_locked = False


def short_press(event, value, condition):
    """Enables throttle setting hold / disabling of mode selection.

    :param event the physical input event being processed
    :param value value extracted from the event
    :param condition activation condition for this action
    """
    global throttle_locked
    if value.current and throttle_locked == False:
        vjoy = gremlin.joystick_handling.VJoyProxy()
        joy = gremlin.input_devices.JoystickProxy()
        vjoy[vjoy_device_id].axis(vjoy_throttle_id).value = \
                joy[phys_device_id].axis(phys_throttle_id).value
        throttle_locked = True
    elif value.current and throttle_locked == True:
        vjoy = gremlin.joystick_handling.VJoyProxy()
        throttle_locked = False
        vjoy[vjoy_device_id].button(vjoy_ab_button).is_pressed = False


def long_press(event, value, condition):
    """Enables 100% throttle and AB activation.

    :param event the physical input event being processed
    :param value value extracted from the event
    :param condition activation condition for this action
    """
    global throttle_locked
    if value.current:
        vjoy = gremlin.joystick_handling.VJoyProxy()
        vjoy[vjoy_device_id].axis(vjoy_throttle_id).value = max_throttle_value
        vjoy[vjoy_device_id].button(vjoy_ab_button).is_pressed = True
        throttle_locked = True


# Tempo container, which holds both of the above actions and executes them
# based on the duration the button is being held down
cruise_mode_container = gremlin.actions.Tempo(
        [
            short_press,
            long_press
        ],
        None,
        0.5
)


@t16000.axis(phys_throttle_id)
def throttle(event, vjoy):
    if not throttle_locked:
        vjoy[vjoy_device_id].axis(vjoy_throttle_id).value = event.value


@t16000.button(phys_cruise_button)
def cruise_mode(event, vjoy):
    value = gremlin.actions.Value(event.is_pressed)
    cruise_mode_container(event, value)

