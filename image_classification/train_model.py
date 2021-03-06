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

Training the navigation model.
"""
import os
import numpy as np
import random
import re
from time import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

MODEL_NAME = f"navigation_model_{int(time())}.model"
EPOCHS = 100

WIDTH = 482
HEIGHT = 808

training_data = np.load("navigation_checkpoint_1000.npy")

# Shuffle the data
np.random.shuffle(training_data)

# Get 20 percent of the data for testing, use the remaining for training. 
training_percent = int(training_data.shape[0] * 0.2)

# Testing data is 'training_percent' percent of all the data. The remaining
# data is used for training.
test = training_data[:training_percent]  
train = training_data[training_percent:]

# Separate images and labels
train_images = np.array([i[0] for i in train])
train_labels = np.array([i[1] for i in train])

# Set pixel values for images to between 0 and 1.
train_images = train_images / 255.0 

# Separate images and labels
test_images = np.array([i[0] for i in test])
test_labels = np.array([i[1] for i in test])

# Set pixel values for images to between 0 and 1.
test_images = test_images / 255.0

# Image Classification Model
model = keras.Sequential([
    Flatten(input_shape=train_images.shape[1:]),
    Dense(128, activation=tf.nn.relu),
    Dense(train_labels.shape[1], activation=tf.nn.softmax)
])

# Tensorboard for model
tensorboard = TensorBoard(log_dir=f"logs/{MODEL_NAME}")
    
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    
# Train model
model.fit(train_images, train_labels, epochs=EPOCHS, callbacks=[tensorboard])
        
# Save model
keras.models.save_model(model, MODEL_NAME)
model.save(MODEL_NAME)
