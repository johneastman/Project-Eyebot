"""This is an artificial agent that plays "Fallout: New Vegas".

NOTICE: This file has been modified from its original version. See below:
coding: utf-8
Object Detection Demo
License: Apache License 2.0 (https://github.com/tensorflow/models/blob/master/LICENSE)
source: https://github.com/tensorflow/models

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
import numpy as np
import os
import tensorflow as tf
import time
from PIL import Image, ImageGrab
import cv2

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

import direct_keys  # direct_keys.py
    
# Load the navigation model

# Path to label map
PATH_TO_LABELS = os.path.join(os.getcwd(), "fallout_inference_graph\\labelmap.pbtxt")

# Path to frozen detection graph.
PATH_TO_CKPT = os.path.join(os.getcwd(), "fallout_inference_graph\\frozen_inference_graph.pb")

# Number of objects in the model
NUM_CLASSES = 5

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, "rb") as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# Label maps map indices to category names, so that when our convolution network
# predicts `5`, we know that this corresponds to `airplane`.  Here we use internal
# utility functions, but anything that returns a dictionary mapping integers to
# appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

enemy_attack_confidence = 0.94

bounding_box = (8, 32, 808, 482)
WIDTH =  bounding_box[2]
HEIGHT = bounding_box[3]

within_range = False  # Whether the agent is a certain distance from an enemy or not
is_combat_mode = False
nav_timer_reset = False

back_key = direct_keys.S
forward_key = direct_keys.W

prev_key, prev_mouse = ("W", "none")
model = tf.keras.models.load_model("navigation.model")

start_time = time.time()

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        while True:

            # Capture the screen
            screen = cv2.resize(np.asarray(ImageGrab.grab(bbox=bounding_box)), (WIDTH, HEIGHT))

            # Convert the screen to a numpy array
            image_np = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            
            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            
            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)

            # Our code starts here
            enemy_info = []
            for i, b in enumerate(boxes[0]):
                if scores[0][i] >= enemy_attack_confidence:
                    mid_x = ((boxes[0][i][1] + boxes[0][i][3]) / 2)
                    mid_y = ((boxes[0][i][0] + boxes[0][i][2]) / 2)

                    # Distance 
                    distance = round((1 - (boxes[0][i][3] - boxes[0][i][1])) ** 4, 3)
                    enemy_info.append((distance, mid_x, mid_y))

            if len(enemy_info) > 0:  # If an enemy has been detected
            
                is_combat_mode = True
                
                direct_keys.release_key(forward_key)
                
                # Retrieve the coordinates of the closest enemy
                closest_enemy_distance, mid_x, mid_y = sorted(enemy_info, key=lambda x: x[0])[0]
                
                # cv2.circle(image_np,(int(mid_x * WIDTH), int(mid_y * HEIGHT)), 3, (0,0,255), -1)
                
                # The game is being played in a window smaller than the resolution
                # of the monitor. This gets the coordinates of the enemy-detection
                # box relative to the monitor.
                # This logic is based on this tutorial:
                # https://pythonprogramming.net/acquiring-vehicle-python-plays-gta-v/
                x_move = mid_x - 0.5
                y_move = mid_y - 0.5
                
                # How much the mouse needs to move
                delta_x = int((x_move / 0.5) * WIDTH)
                delta_y = int((y_move / 0.5) * HEIGHT)
                
                # Move mouse
                direct_keys.press_mouse(dx=delta_x, dy=delta_y)
                
                # Shoot
                direct_keys.press_mouse("left_down")
                time.sleep(0.1)
                direct_keys.press_mouse("left_up")
                
                # Move the agent backwards if the enemy gets too close
                if closest_enemy_distance < 0.60:
                    direct_keys.press_key(back_key)
                    within_range = True
                else:
                    within_range = False
                    
            # Navigation Agent
            else:
                if not nav_timer_reset:
                    navigation_start_time = time.time()
                    nav_timer_reset = True
                
                direct_keys.press_key(forward_key)

            if is_combat_mode and time.time() - navigation_start_time >= 3:
                direct_keys.key_sequence(f"~player.SetAngle X 0\n~".upper())
                navigation_start_time = time.time()
                is_combat_mode = False
                nav_timer_reset = False
                
            # Release the back key if the enemy is no longer within range
            if not within_range:
                direct_keys.release_key(back_key)

            cv2.imshow("window", image_np)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
