import tensorflow as tf
import cv2
import numpy as np
from PIL import ImageGrab
import time
import sys

sys.path.insert(0, "..")

import direct_keys  # direct_keys.py

model = tf.keras.models.load_model("navigation.model")

actions = [("W", "right"),   ("W", "left"),   ("W", "none"),
           ("A", "right"),   ("A", "left"),   ("A", "none"),
           ("S", "right"),   ("S", "left"),   ("S", "none"),
           ("D", "right"),   ("D", "left"),   ("D", "none"),
           ("NIL", "right"), ("NIL", "left"), ("NIL", "none")]

def predict(image):
    
    new_screen = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    new_screen = cv2.resize(new_screen, (450, 800))
    action = model.predict([new_screen.reshape(1, 450, 800)])
    return action[0]
    
bounding_box = (8, 32, 808, 482)
WIDTH =  bounding_box[2]
HEIGHT = bounding_box[3]

prev_key, prev_mouse = ("W", "none")

to_move = {"right": -100,
           "left":  100,
           "none":  0}

PAUSED = False
while True:

    if direct_keys.is_key_pressed("P"):
        PAUSED = not PAUSED
        
        if PAUSED:
            for key in ["W", "A", "S", "D"]:
                direct_keys.release_key(key)
        
        time.sleep(1)

    screen = cv2.resize(np.asarray(ImageGrab.grab(bbox=bounding_box)), (WIDTH, HEIGHT))
    image_np = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    predicted_action = predict(image_np)
    key, mouse = actions[np.argmax(predicted_action)]
    
    if not PAUSED:
    
        # Release the previously-pressed key
        direct_keys.release_key(prev_key)
        
        direct_keys.press_key(key)
        direct_keys.press_mouse(dx=to_move[mouse])
        
        # Update the previous key and mouse presses
        prev_key = key
        prev_mouse = mouse
    
    cv2.imshow("window", image_np)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break