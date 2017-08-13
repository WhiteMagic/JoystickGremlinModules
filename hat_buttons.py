import gremlin

t16000 = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)

# Action triggered when the hat is moved up, causing vJoy 1 button 1 to
# be pressed and released
hat_up_remap = gremlin.actions.Basic(
    gremlin.actions.Factory.remap_input(
        gremlin.common.InputType.JoystickHat,
        gremlin.common.InputType.JoystickButton,
        1,
        1
    ),
    gremlin.actions.HatButton([(0, 1)])
)
# Action triggered when the hat is moved down, causing vJoy 1 button 2 to
# be pressed and released
hat_down_remap = gremlin.actions.Basic(
    gremlin.actions.Factory.remap_input(
        gremlin.common.InputType.JoystickHat,
        gremlin.common.InputType.JoystickButton,
        1,
        2
    ),
    gremlin.actions.HatButton([(0, -1)])
)


@t16000.hat(1, always_execute=False)
def t16000_hat(event, vjoy):
    """Map hat up direction to vjoy button 1."""
    hat_up_remap(event, gremlin.actions.Value(event.value))
    hat_down_remap(event, gremlin.actions.Value(event.value))


