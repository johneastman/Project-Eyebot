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

This file sets up the object-detection data and trains the model. The specific
details can be found in the comments.
"""
import os
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import shutil
import errno
from distutils.dir_util import copy_tree
import re

def get_full_path(relative_path):
    """Get the absolute path for a relative path."""
    return os.path.join(os.getcwd(), relative_path)
    
def execute_command(command):
    """Execute a command."""
    os.system(command)
    
def create_directory(path):
    """Create a directory.
    
    Returns true if the directory was created. Returns false if the directory
    being created already exists.
    """
    if not os.path.isdir(path):
        os.mkdir(path)
        return True
    else:
        print(f"{path} already exists.")
        return False
    
# Constants and paths
FALLOUT_IMAGES_NAME = "Fallout_images"
FALLOUT_TRAINING_NAME = "Fallout_training"
    
ALL_IMAGES = get_full_path("images")  # Where all the image and xml files are
FALLOUT_IMAGES = get_full_path("Fallout_images")
TEST_CSV = os.path.join(FALLOUT_IMAGES, "test_labels.csv")
TRAIN_CSV = os.path.join(FALLOUT_IMAGES, "train_labels.csv")
TEST_RECORD = os.path.join(FALLOUT_IMAGES, "test.record")
TRAIN_RECORD = os.path.join(FALLOUT_IMAGES, "train.record")

# Path to the tensorflow object-detection folder.
OBJECT_DETECTION_PATH = r"D:\Coding\Tensorflow\models\research\object_detection"

#----------------------+
# Fallout_images Setup |
#----------------------+

# Where the testing images will go
testing_path = os.path.join(FALLOUT_IMAGES, "test")

# Where the training images will go
training_path = os.path.join(FALLOUT_IMAGES, "train")

# Create directories. Exit if any already exist
for dir in [FALLOUT_IMAGES, testing_path, training_path]:
    if not create_directory(dir):
        sys.exit(1)

# Call "move_images.py" to separate images into training and testing directories
command = f"python move_images.py {ALL_IMAGES} {testing_path} {training_path}"
execute_command(command)

# Put xml data into csv files
command = f"python xml_to_csv.py {testing_path} {TEST_CSV}"
execute_command(command)

command = f"python xml_to_csv.py {training_path} {TRAIN_CSV}"
execute_command(command)

# Convert training data in csv files into record files
command = f"python generate_tfrecord.py --csv_input={TEST_CSV} --output_path={TEST_RECORD} --image_dir={testing_path}"
execute_command(command)

# Convert testing data in csv files into record files
command = f"python generate_tfrecord.py --csv_input={TRAIN_CSV} --output_path={TRAIN_RECORD} --image_dir={training_path}"
execute_command(command)

#------------------------+
# Fallout_training Setup |
#------------------------+

# Lables used for objects in images
labels = ["gecko", "bloatfly", "deathclaw", "scorpion", "radscorpion"]
NUM_CLASSES = len(labels)


NUM_STEPS = 100000
NUM_EXAMPLES = int(len(os.listdir(testing_path)) / 2)
FINE_TUNE_CHECKPOINT = r"faster_rcnn_inception_v2_coco_2018_01_28/model.ckpt" 
FALLOUT_TRAINING = get_full_path("Fallout_training")
LABEL_MAP_PATH = os.path.join(FALLOUT_TRAINING, "labelmap.pbtxt")
INPUT_PATH = TEST_RECORD

MODEL_NAME = "faster_rcnn_inception_v2_coco.config"
CONFIG_FILES = r"D:\Coding\Tensorflow\models\research\object_detection\samples\configs"

# Load the specified model template file, which in this case is the value of 
# 'MODEL_NAME'. That file is a template, and various parameters need to be
# filled in. The following lines of code loads the template and fills in the 
# missing values.
if not os.path.isdir(FALLOUT_TRAINING):
    os.mkdir(FALLOUT_TRAINING)
    
# Writing lables to "labelmap.pbtxt" Each label in that file takes the following
# form:
#   item {
#       id: 1
#       name: 'gecko'
#   }
with open(LABEL_MAP_PATH, "w") as labelmap:
    for i, label in enumerate(labels, 1):

        # Create an entry in the file for each label
        item = "item {{\n  id: {}\n  name: '{}'\n}}\n\n".format(i, label)
        labelmap.write(item)

# Get config file from tensorflow object-detection models
config_src = os.path.join(CONFIG_FILES, MODEL_NAME)
shutil.copy(config_src, FALLOUT_TRAINING)
      
# Open the object-detection template. 
with open(os.path.join(FALLOUT_TRAINING, MODEL_NAME), "r") as config_file:
    contents = [line for line in config_file]

# Update fields with information relevant to this model.
new_contents = []
for line in contents:

    if line.startswith("#"):
        # Comments
        new_contents.append(line)
        continue

    if "num_classes:" in line:
        num_classes_str = r"num_classes: {}\n".format(NUM_CLASSES)
        line = re.sub(r"num_classes.*?\n", num_classes_str, line, flags=re.DOTALL)
        
    if "fine_tune_checkpoint:" in line:
        fine_tune_checkpoint_str = "fine_tune_checkpoint: \"{}\"\n".format(FINE_TUNE_CHECKPOINT)
        line = re.sub(r"fine_tune_checkpoint.*?\n", fine_tune_checkpoint_str, line, flags=re.DOTALL)
        
    if "num_steps:" in line:
        num_steps_str = r"num_steps: {}\n".format(NUM_STEPS)
        line = re.sub(r"num_steps.*?\n", num_steps_str, line, flags=re.DOTALL)
        
    if "num_examples:" in line:
        num_examples_str = r"num_examples: {}\n".format(NUM_EXAMPLES)
        line = re.sub(r"num_examples.*?\n", num_examples_str, line, flags=re.DOTALL)

    new_contents.append(line)
    
contents = "".join(new_contents)
    
# Retain brackets when .format is run on filecontents.
contents = contents.replace("{", "{{")
contents = contents.replace("}", "}}")
contents = re.sub(r"\"PATH_TO_BE_CONFIGURED/.*?\n", "{}\n", contents, flags=re.DOTALL)

contents = contents.format(f"\"Fallout_images/train.record\"",
                           "\"Fallout_training/labelmap.pbtxt\"",
                           "\"Fallout_images/test.record\"",
                           "\"Fallout_training/labelmap.pbtxt\"")

# Overwrite existing file with updated information
with open(os.path.join(FALLOUT_TRAINING, MODEL_NAME), "w") as config_file:
    config_file.write(contents)

# Move the data in the 'FALLOUT_IMAGES' and 'FALLOUT_TRAINING' directories to
# the object detection directory in the Tensorflow folder.
try:
    shutil.move(FALLOUT_IMAGES, OBJECT_DETECTION_PATH)
    shutil.move(FALLOUT_TRAINING, OBJECT_DETECTION_PATH)
except:
    pass

#------------------------------+
# Train Object Detection Model |
#------------------------------+

# Change to directory with object detection files
os.chdir(OBJECT_DETECTION_PATH)

# Train the model
command = f"python train.py --logtostderr --train_dir=Fallout_training_dir/ --pipeline_config_path=Fallout_training/{MODEL_NAME}"
execute_command(command)
