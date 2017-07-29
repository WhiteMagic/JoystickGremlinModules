import gremlin

t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)

# Flag tracking the state of the afterburner
g_ab_active = False

# Macro executed to activate the AB
start_macro = gremlin.macro.Macro()
start_macro.press("Left Shift")

# Macro executed to stop the AB
stop_macro = gremlin.macro.Macro()
stop_macro.release("Left Shift")


@t16000m.button(1)
def cycle_ab(event):
    global g_ab_active
    if event.is_pressed:
        if g_ab_active:
            gremlin.macro.MacroManager().add_macro(stop_macro, None, event)
        else:
            gremlin.macro.MacroManager().add_macro(start_macro, None, event)
        g_ab_active = not g_ab_active

