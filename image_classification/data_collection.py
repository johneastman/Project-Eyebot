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

Collecting data for the navigation model. This file generates one-hot arrays
associated with each keyboard-mouse pair. When the screen is captures, this
script checks what key is pressed on the keyboard and what mouse movement is
active (e.g., left, right, or none), and pairs the image and array together
before saving.
"""
import win32api
import cv2
import numpy as np
from PIL import ImageGrab
import time
import sys
import os
from collections import OrderedDict
import numpy as np
import direct_keys  # direct_keys.py

sys.path.insert(0, "..")

BOUNDING_BOX = (8, 32, 808, 482)
PAUSE_KEY = "P" # <-- Set the key that pauses the program here
SHOW_WINDOW = False
PAUSED = True

def is_key_pressed(key):
    """Check if a key is pressed."""
    return win32api.GetAsyncKeyState(ord(key)) != 0
    
def capture_screen(bounding_box):
    """Capture the screen and process the image."""
    screen = np.array(ImageGrab.grab(bbox=bounding_box))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    screen = cv2.resize(screen, (75, 133))
    return screen

def get_current_checkpoint():
    """Get the current checkpoint value.
    
    If recording happens over multiple sessions, this ensures that previous
    data will not get overwritten.
    """
    checkpoints = [file for file in os.listdir("checkpoints/") if file.endswith(".npy")]
    
    if len(checkpoints) == 0:
        # No checkpoint files found. Start at 0.
        return 0
    
    # Get the id of each checkpoint and return the largest one plus 1 (for 
    # the new checkpoint).
    checkpoints = [checkpoint.rsplit(".", 1)[0] for checkpoint in checkpoints]
    max_checkpoint = max(int(checkpoint.rsplit("_", 1)[1]) for checkpoint in checkpoints)
    return max_checkpoint + 1


class Output:
    """This formats output hot-key arrays for each keys in the input."""
    def __init__(self, keys):
        """Initialize hot-key arrays for each key in 'keys'.
        
        Each array is the length of 'keys'. In each array, only one "bit" can
        be on for each, which is determined by matching the key with its index
        in the array of keys. Example:
            
            keys = ["W", "S", "A", "D", "NIL"]
            
            # The index of "W" is 0, so the zeroth element in the array
            # for W will be 1, and the remaining elements will be 0.
            W = [1, 0, 0, 0, 0]
            
            # The index of "S" is 1, so the second element in the array
            # for S will be 1, and the remaining elements will be 0.
            S = [0, 1, 0, 0, 0]
        """
        self.keys = keys
        self.num_keys = len(keys)
        
        # The order with which keys are pressed is important.
        self.keys_output = OrderedDict()
        for i, key in enumerate(keys):
            self.keys_output[key] = [int(i == keys.index(key)) 
                                     for i in range(self.num_keys)]

    def get_output(self):
        """Return the key-mouse pair that is active."""
        # Get the direction the mouse is moving (left, right, or not moving)
        mouse_direction = direct_keys.get_mouse_direction()
    
        for (key, mouse_dir), value in self.keys_output.items():
        
            # 'input' is a tuple, where the first element is a key and the
            # second element is a mouse direction ("left", "right", or "none")
            
            try:
                # Find the key-direction pair that matches the currently-pressed
                # key and the current mouse direction and return the associated
                # hot-key array.
                if is_key_pressed(key) and mouse_dir == mouse_direction:  
                    return value
            # NIL is not a key; it denotes that no key was pressed. Because this
            # implementation of 'is_key_pressed' required characters, a type
            # error will be rasied with 'NIL' is passed as a parameter.
            except TypeError:
                # Second element in 'input' is mouse direction
                return self.keys_output[("NIL", mouse_direction)]


if __name__ == "__main__":

    # Pair each input (keys, mouse) combination with a one-hot array
    input_combinations = [("W", "right"),   ("W", "left"),   ("W", "none"),
                          ("A", "right"),   ("A", "left"),   ("A", "none"),
                          ("S", "right"),   ("S", "left"),   ("S", "none"),
                          ("D", "right"),   ("D", "left"),   ("D", "none"),
                          ("NIL", "right"), ("NIL", "left"), ("NIL", "none")]
    output_object = Output(input_combinations)

    training_data = []
    checkpoint = get_current_checkpoint()
    print(checkpoint)

    filename_template = "checkpoints/navigation_training_data_{}.npy"
    filename = filename_template.format(checkpoint)
    
    print(f"Program is paused. Press {PAUSE_KEY} to begin")
    while True:
    
        # Pause the script from recording
        if is_key_pressed(PAUSE_KEY):
            PAUSED = not PAUSED
            
            if PAUSED:
                print("PAUSED")
            else:
                print("UNPAUSED")
            time.sleep(1)

        if not PAUSED:
            screen = capture_screen(BOUNDING_BOX)
            output = output_object.get_output()

            training_data.append([screen, output])

            # Save a checkpoint of the data
            if len(training_data) == 1000:
                print(f"saving {filename} to disk...", end="")

                np.save(filename, training_data)
                training_data = []
                checkpoint += 1
                
                # Update the filename for the next checkpoint file
                filename = filename_template.format(checkpoint)

                print("done")

            # Only show what has been recorded if this setting is "True"
            if SHOW_WINDOW:
                cv2.imshow("window", screen)

                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break
