import threading
import time

import gremlin

t16000 = gremlin.input_devices.JoystickDecorator(
    "T.16000M",
    72331530,
    "Default"
)

# Maximum duration of a "short" press
g_timeout = 0.3
# Seconds to hold the button pressed
g_hold_time = 0.1
# Seconds to wait between releasing and pressing the button again
g_pause_time = 0.1
# Timer object triggering the "long press"
g_timer = None
# Flag indicating if the pulse action is running or should be stopped
g_is_running = True


# Assumption same key for both short and long press, but long press will start
# to pulse the key instead of just holding it down.


def pulse(vjoy, btn_id):
    """Runs the long press macro repeatedly with a pause in between executions.
    
    :param vjoy the vJoy proxy object
    :param btn_id the id of the button to press and release in the pulse
    """
    global g_is_running
    g_is_running = True
    while g_is_running:
        vjoy[1].button(btn_id).is_pressed = True
        time.sleep(g_hold_time)
        vjoy[1].button(btn_id).is_pressed = False
        time.sleep(g_pause_time)
        

@t16000.button(1)
def button1(event, vjoy):
    # Id of the button to press or pulse
    btn_id = 5
    global g_is_running, g_timer
    if event.is_pressed:
        # Press the button
        vjoy[1].button(btn_id).is_pressed = True

        # Start a timer so we can transition to pulsing when the button
        # is held down long enough
        g_timer = threading.Timer(g_timeout, lambda: pulse(vjoy, btn_id))
        g_timer.start()
    else:
        # Terminate the pulsing if needed and remove the timer if needed
        g_is_running = False
        if g_timer:
            g_timer.cancel()
        # Ensure the button is released
        vjoy[1].button(btn_id).is_pressed = False


@t16000.button(2)
def button2(event, vjoy):
    btn_id = 6
    global g_is_running, g_timer
    if event.is_pressed:
        vjoy[1].button(btn_id).is_pressed = True
        g_timer = threading.Timer(g_timeout, lambda: pulse(vjoy, btn_id))
        g_timer.start()
    else:
        g_is_running = False
        if g_timer:
            g_timer.cancel()
        vjoy[1].button(btn_id).is_pressed = False


@t16000.button(4)
def button4(event, joy, vjoy):
    btn_id = 6
    global g_is_running, g_timer
    if event.is_pressed and joy[1].button(3).is_pressed:
        vjoy[1].button(btn_id).is_pressed = True
        g_timer = threading.Timer(g_timeout, lambda: pulse(vjoy, btn_id))
        g_timer.start()
    else:
        g_is_running = False
        if g_timer:
            g_timer.cancel()
        vjoy[1].button(btn_id).is_pressed = False
