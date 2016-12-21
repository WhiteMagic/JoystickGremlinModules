import gremlin

# Joystick decorator
t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)

# Mapping from hat directions (X, Y) to vJoy button
button_map = {
    (0, 1): 10,
    (1, 0): 11,
    (0, -1): 12,
    (-1, 0): 13
}


@t16000m.hat(1)
def hat1_to_buttons(event, vjoy):
    for key, value in button_map.items():
        if key == event.value:
            vjoy[1].button(value).is_pressed = True
        else:
            vjoy[1].button(value).is_pressed = False
