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

Separate a folder of images into testing and training sets.

For object detection, every image has an associated xml that holds the coordinates
of objects in the image. The purpose of this file is to split up that data into 
two data sets: training data and testing data.

Every image (jpeg) and associated xml file share the same name. Because of this,
a list of unique names can be put in a list, and those filenames can be shuffled
and distributed into training and testing datasets. After this has been completed, 
these filenames can be reassociated with a jpeg and xml file, which are both then
moved into a training or testing directory.
"""
import os
import sys
import random
import shutil

images_path = sys.argv[1]
testing_path = sys.argv[2]
training_path = sys.argv[3]

# Get a list of unique filenames.
images = [image.rsplit(".", 1)[0] for image in os.listdir(images_path) if image.endswith(".xml")]

random.shuffle(images)  # Shuffle the data

# 20 percent of the images are reserved for testing. The remaining 80 percent 
# are used for training.
percent = int(len(images) * 0.2)

testing_images = images[:percent]
training_images = images[percent:]

# Move the images and their associated xml files into their specified
# directories (i.e., training set or testing set).
for path, images in [(testing_path, testing_images), (training_path, training_images)]:
    
    if not os.path.isdir(path):
        # If the training or testing directories don't exist, create them.
        os.mkdir(path)
    
    for image in images:

        # Add file extensions to 'image' (an image and xml filename)
        jpeg = f"{image}.jpeg"
        xml = f"{image}.xml"
    
        # Get the source of the image and xml files
        old_jpeg_path = os.path.join(images_path, jpeg)
        old_xml_path = os.path.join(images_path, xml)
        
        # Get the destination of the image and xml files
        new_jpeg_path = os.path.join(path, jpeg)
        new_xml_path = os.path.join(path, xml)
        
        # Move both files to their specified directory.
        shutil.move(old_jpeg_path, new_jpeg_path)
        shutil.move(old_xml_path, new_xml_path)
