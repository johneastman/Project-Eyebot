"""Capstone Demo."""

from direct_keys import *

def countdown(_from, to):
    """
    Countdown from 'from' to 'to' in seconds.
    """
    for i in range(_from, to, -1):
        print(f"{i}...")
        time.sleep(1)
        
def choose_from_distribution(distribution):
    values, weights = map(list, zip(*distribution))
    return random.choices(values, weights=weights, k=1)[0]
        
def move_mouse_over_time():
    look = choose_from_distribution(look_distribution)
    
    direction = 10

    if look != None:
        if look == "left":
            direction *= -1
        
        for i in range(50):
            press_mouse(dx=direction, dy=0)
            time.sleep(MOUSE_SLEEP)
        
        
keys_distribution = [("W", 0.80), # forward
                     ("A", 0.09), # left
                     ("S", 0.02), # back
                     ("D", 0.09)] # right

mouse_distribution = [("left_down", 0.2),
                      ("right_down", 0.2),
                      (None,0.6) ]
                      
look_distribution = [("left", 0.2),
                     ("right", 0.2),
                     (None, 0.6) ]

if __name__ == '__main__':

    countdown(5, 0)
    
    while True:
        key = choose_from_distribution(keys_distribution)
        mouse = choose_from_distribution(mouse_distribution)
        
        
        press_key(key)
        move_mouse_over_time()
        
        if mouse != None:
            press_mouse(mouse)
            print(mouse)
            
            if mouse == "left_down":
                time.sleep(LEFT_CLICK_TIME)
                press_mouse("left_up")
            else:
                time.sleep(RIGHT_CLICK_TIME)
                press_mouse("right_up")
        
        if key == "W":
            time.sleep(2)
        else:
            time.sleep(1)
        
        release_key(key)