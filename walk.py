import gremlin

gamepad = gremlin.input_devices.JoystickDecorator(
        name="Logitech Dual Action",
        device_id=74301974,
        mode="Default"
)


class MotionControl:

    walking_threshold = 0.25
    running_threshold = 0.75

    key_direction_map = {
        "W": [-walking_threshold, -1.0],
        "S": [walking_threshold, 1.0],
        "A": [-walking_threshold, -1.0],
        "D": [walking_threshold, 1.0]
    }

    def __init__(self):
        self.buttons = {}
        self.macros = {}
        for key, thresholds in MotionControl.key_direction_map.items():
            self.buttons[key] = gremlin.util.AxisButton(
                thresholds[0], thresholds[1]
            )
            self.macros[(key, "start")] = gremlin.macro.Macro()
            self.macros[(key, "start")].action(gremlin.macro.key_from_name(key), True)
            self.macros[(key, "stop")] = gremlin.macro.Macro()
            self.macros[(key, "stop")].action(gremlin.macro.key_from_name(key), False)

        self.forward = lambda x: self.start_stop(
                self.macros[("W", "start")],
                self.macros[("W", "stop")],
                x
            )
        self.backward = lambda x: self.start_stop(
                self.macros[("S", "start")],
                self.macros[("S", "stop")],
                x
            )
        self.left = lambda x: self.start_stop(
                self.macros[("A", "start")],
                self.macros[("A", "stop")],
                x
            )
        self.right = lambda x: self.start_stop(
                self.macros[("D", "start")],
                self.macros[("D", "stop")],
                x
            )

    def start_stop(self, macro_start, macro_stop, is_pressed):
        if is_pressed:
            macro_start.run()
        else:
            macro_stop.run()

    def forward_backward(self, value):
        self.buttons["W"].process(value, self.forward)
        self.buttons["S"].process(value, self.backward)

    def left_right(self, value):
        self.buttons["A"].process(value, self.left)
        self.buttons["D"].process(value, self.right)

control = MotionControl()

@gamepad.axis(4)
def forward_backward(event):
    control.forward_backward(event.value)

@gamepad.axis(3)
def left_right(event):
    control.left_right(event.value)
