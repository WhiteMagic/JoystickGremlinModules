import gremlin

t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)

g_ab_active = False

# Macro executed when the activation zone is entered by the axis
start_macro = gremlin.macro.Macro()
start_macro.action(gremlin.macro.Keys.LShift, True)

# Macro executed when the activation zon is left by the axis
stop_macro = gremlin.macro.Macro()
stop_macro.action(gremlin.macro.Keys.LShift, False)


@t16000m.button(1)
def cycle_ab(event):
    global g_ab_active
    if event.is_pressed:
        if g_ab_active:
            stop_macro.run()
        else:
            start_macro.run()
        g_ab_active = not g_ab_active

