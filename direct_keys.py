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

MOUSE_SLEEP = 0.001


def get_mouse_pos():
    _, _, pos = win32gui.GetCursorInfo()
    return pos

# Used for detecting whether the mouse has moved or not
previous_position = get_mouse_pos()

direct_keys = {"A": 0x1E,
               "B": 0x30,
               "C": 0x2E,
               "D": 0x20,
               "E": 0x12,
               "F": 0x21,
               "G": 0x22,
               "H": 0x23,
               "I": 0x17,
               "J": 0x24,
               "K": 0x25,
               "L": 0x26,
               "M": 0x32,
               "N": 0x31,
               "O": 0x18,
               "P": 0x19,
               "Q": 0x10,
               "R": 0x13,
               "S": 0x1F,
               "T": 0x14,
               "U": 0x16,
               "V": 0x2F,
               "W": 0x11,
               "X": 0x2D,
               "Y": 0x15,
               "Z": 0x2C,
               ".": 0x34,
               " ": 0x39,
               "1": 0x02,
               "2": 0x03,
               "3": 0x04,
               "4": 0x05,
               "5": 0x06,
               "6": 0x07,
               "7": 0x08,
               "8": 0x09,
               "9": 0x0A,
               "0": 0x0B,
               "\n": 0x1C,
               "~": 0x29}

# direct_keys  = {W: 0x11, A: 0x1E, S: 0x1F, D: 0x20}

mouse_clicks = {"left_down": 0x2, "left_up": 0x4,
                "right_down":0x8, "right_up": 0x10, "no_click": 0}
                
def is_key_pressed(key):
    return win32api.GetAsyncKeyState(ord(key)) != 0

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
    
def key_sequence(string):
    """Press all the keyboard keys in a string of keys.
    
    For example, if you wanted to type "Hello, world", this function would
    iterate over each character in the string and press that key.
    """
    for key in string:
        press_key(key)
        time.sleep(0.1)
        release_key(key)
   
def move_mouse_over_time(dx):  
    for i in range(50):
        press_mouse(dx=dx)
        time.sleep(MOUSE_SLEEP)


def get_mouse_direction():
    """Return the direction the mouse is moving.
    
    Note: Only detects left, right, or no movement
    
    "right" -> Moving right
    "left"  -> Moving left
    "none"  -> Mouse is not moving
    """
    global previous_position
    
    prev_x, prev_y = previous_position
    curr_x, curr_y = get_mouse_pos()
    
    # Update the previous position of the mouse
    previous_position = (curr_x, curr_y)
    
    # Width of screen. Minus 1 because resolution goes from 0 to (width - 1)
    # e.g., if width is 1920, mouse goes from 0 to 1919
    if (curr_x > prev_x or curr_x == win32api.GetSystemMetrics(0) - 1) and curr_y != prev_y:
        return "right"
    elif (curr_x < prev_x or curr_x == 0) and curr_y != prev_y:
        return "left"
    
    return "none"
    
    # return not (prev_x == curr_x and prev_y == curr_y)

if __name__ == "__main__":
    
    while True:
        direction = get_mouse_direction()
        print(direction)
        time.sleep(0.1)