"""Utility for simulating keyboard and mouse input.

Copyright 2018 Caitlin Chapdelaine and John Eastman

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# Key Codes: http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
import ctypes
import time
import random
import win32gui
import win32api

# Keys
W = "W"
A = "A"
S = "S"
D = "D"

direct_keys  = {W: 0x11, A: 0x1E, S: 0x1F, D: 0x20}
virtual_keys = {W: 0x57, A: 0x41, S: 0x53, D: 0x44}

mouse_clicks = {"left_down": 0x2, "left_up": 0x4,
                "right_down":0x8, "right_up": 0x10, "no_click": 0}

def press_mouse(button="no_click", dx=0, dy=0):
    # mouse_event usage:
    # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event
    if button not in mouse_clicks:
        raise KeyError(f"{button} is an invalid button")
    
    mouse_button_hex_code = mouse_clicks[button]
    if dx != 0 or dy != 0:
        mouse_button_hex_code |= 0x0001
    ctypes.windll.user32.mouse_event(mouse_button_hex_code, dx, dy, 0, 0)

def press_key(key):
    # Get the direct-key hex-code associated with 'key'.
    # keybd_event usage:
    # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-keybd_event
    if key not in direct_keys:
        raise KeyError(f"{key} is an invalid key")
    key_hex_code = direct_keys[key]
    ctypes.windll.user32.keybd_event(0, key_hex_code, 0, 0)

def release_key(key):
    # Get the direct-key hex-code associated with 'key'.
    # keybd_event usage:
    # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-keybd_event
    # 0x0002 flag indicates that key is being released.
    if key not in direct_keys:
        raise KeyError(f"{key} is an invalid key")
    
    key_hex_code = direct_keys[key]
    ctypes.windll.user32.keybd_event(0, key_hex_code, 0x0002, 0)

def is_key_pressed(key):
    """Get the virtual key code for a key and check if that key is pressed.

    Only works with virtual key codes (not direct key codes). For example, for
    "W", 0x57 (virtual) will work, but 0x11 (direct) will not.

    Virtual key codes:
    https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes
    """
    virtual_key_hex_code = virtual_keys[key]
    return ctypes.windll.user32.GetKeyState(virtual_key_hex_code) > 1

def move_mouse(x, y):
    pos = (x, y)
    win32api.SetCursorPos(pos)
  
def get_mouse_pos():
    _, _, pos = win32gui.GetCursorInfo()
    return pos

