"""Screen capture.

MIT License

Copyright (c) 2018 jeastmanGIT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import numpy as np
from PIL import ImageGrab
import cv2
import ctypes
import time
from random import random

screen_color = {"default": 0,
                "rgb":     cv2.COLOR_BGR2RGB,
                "grey":    cv2.COLOR_BGR2GRAY}

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img

def save_screenshot(screen, filename):
    print(f"Saving {filename}")
    cv2.imwrite(filename, cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))

def screen_record(bounding_box, color_key="default"): 
    
    color = screen_color[color_key]
    while True:
        screen = np.array(ImageGrab.grab(bbox=bounding_box))
        cv2.imshow("window", cv2.cvtColor(screen, color))
        filename = f"Geckos/{time.time()}_{random()}.jpeg"
        save_screenshot(screen, filename)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    for i in range(6, 0, -1):
        print(i)
        time.sleep(1)
    screen_record((8, 32, 808, 482), color_key="rgb")
