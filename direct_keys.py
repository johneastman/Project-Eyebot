"""Copyright 2018 Caitlin Chapdelaine and John Eastman

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---

This is a utility for simulating keyboard and mouse input.

Useful information on how to use the keybd_event function:
https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-keybd_event

Usefun information on how to use the mouse_event function:
https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event

Windows keyboard key codes:
http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
"""
import ctypes
import time
import random
import win32gui
import win32api

# Movement keys
W = "W"
A = "A"
S = "S"
D = "D"

MOUSE_SLEEP = 0.005

# Keyboard keys
direct_keys = {"W": 0x11, "A": 0x1E, "S": 0x1F, "D": 0x20}

# Mouse actions
mouse_clicks = {"left_down": 0x2, "left_up": 0x4,
                "right_down":0x8, "right_up": 0x10, "no_click": 0}

def press_mouse(button="no_click", dx=0, dy=0):
    # mouse_event usage:
    if button not in mouse_clicks:
        raise KeyError(f"{button} is an invalid button")
    
    mouse_button_hex_code = mouse_clicks[button]
    if dx != 0 or dy != 0:
        mouse_button_hex_code |= 0x0001
    ctypes.windll.user32.mouse_event(mouse_button_hex_code, dx, dy, 0, 0)

def press_key(key):
    """Press a keyboard key."""
    if key not in direct_keys:
        # Return if the key is not supported.
        return
    key_hex_code = direct_keys[key]
    ctypes.windll.user32.keybd_event(0, key_hex_code, 0, 0)

def release_key(key):
    """Release a pressed keyboard key."""
    if key not in direct_keys:
        # Return if the key is not supported.
        return
    # Get the direct-key hex-code associated with 'key'.
    key_hex_code = direct_keys[key]
    
    # 0x0002 flag indicates that key is being released.
    ctypes.windll.user32.keybd_event(0, key_hex_code, 0x0002, 0)

def move_mouse_over_time(dx):
    """Move the mouse over a period of time.
    
    This allows for smooth mouse movements that would look similar to a human
    moving the mouse.
    """
    for i in range(50):
        press_mouse(dx=dx)
        time.sleep(MOUSE_SLEEP)
