import numpy as np
from PIL import ImageGrab
import cv2
import ctypes

screen_color = {"default": 0,
                "rgb":     cv2.COLOR_BGR2RGB,
                "grey":    cv2.COLOR_BGR2GRAY}

def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img

def save_screenshot(screen, filename):
    cv2.imwrite(filename, screen)

def screen_record(bounding_box, color_key="default"): 
    
    color = screen_color[color_key]
    while True:
        screen = np.array(ImageGrab.grab(bbox=bounding_box))
        cv2.imshow("window", cv2.cvtColor(screen, color))

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

if __name__ == "__main__":
    screen_record((8, 32, 808, 482), color_key="grey")
