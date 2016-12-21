import gremlin

t16000m = gremlin.input_devices.JoystickDecorator(
    name="T.16000M",
    device_id=72331530,
    mode="Default"
)

macro_fight = gremlin.macro.Macro()
macro_fight.tap(gremlin.macro.Keys.KP5)
macro_fight.tap(gremlin.macro.Keys.KP6)
macro_fight.tap(gremlin.macro.Keys.KP6)
macro_fight.tap(gremlin.macro.Keys.KP8)
macro_fight.tap(gremlin.macro.Keys.KP8)

macro_speed = gremlin.macro.Macro()
macro_speed.tap(gremlin.macro.Keys.KP5)
macro_speed.tap(gremlin.macro.Keys.KP8)
macro_speed.tap(gremlin.macro.Keys.KP8)
macro_speed.tap(gremlin.macro.Keys.KP8)

macro_scan = gremlin.macro.Macro()
macro_scan.tap(gremlin.macro.Keys.KP5)
macro_scan.tap(gremlin.macro.Keys.KP4)
macro_scan.tap(gremlin.macro.Keys.KP4)
macro_scan.tap(gremlin.macro.Keys.KP8)
macro_scan.tap(gremlin.macro.Keys.KP8)

@t16000m.hat(1)
def manage_power(event, vjoy, keyboard):
    if keyboard.is_pressed(gremlin.macro.Keys.Space):
        if event.value == (1, 0):
            macro_fight.run()
        elif event.value == (0, 1):
            macro_speed.run()
        elif event.value == (-1, 0):
            macro_scan.run()
    else:
        vjoy[1].hat(1).direction = event.value
