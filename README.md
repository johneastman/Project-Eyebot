# Project Eyebot
Project Eyebot is an artificial agent that plays [Fallout: New Vegas](https://fallout.fandom.com/wiki/Fallout:_New_Vegas). This project was designed and developed by [Caitlin Chapdelaine](https://www.linkedin.com/in/caitlin-chapdelaine-5a625516b/) and [John Eastman](https://www.linkedin.com/in/john-eastman-80a352136/) and was their [Champlain College](https://www.champlain.edu/) Senior project.

# Object Detection
Object detection was used for the combat agent. This entailed training an object detection model on what enemies look like. Data for the object-detection model was collected by screen capturing the game as it was played. The data was then labeled manually using [LabelImg](https://github.com/tzutalin/labelImg) and trained using the Faster RCNN Inception V2 COCO model. 

For the purpose of this project, the object-detection model was trained on the following enemies:

| Bloatfly | Deathclaw | Gecko | Radscorpion | Bark Scorpion |
|:--------:|:---------:|:-----:|:-----------:|:-------------:|
| [![Bloatfly](https://github.com/johneastman/Project-Eyebot/blob/master/images/enemies/Bloatfly.png)](https://fallout.fandom.com/wiki/Bloatfly_(Fallout:_New_Vegas)) | [![Deathclaw](https://github.com/johneastman/Project-Eyebot/blob/master/images/enemies/Deathclaw.png)](https://fallout.fandom.com/wiki/Deathclaw_(Fallout:_New_Vegas)) | [![Gecko](https://github.com/johneastman/Project-Eyebot/blob/master/images/enemies/Gecko.png)](https://fallout.fandom.com/wiki/Gecko_(Fallout:_New_Vegas)) | [![Radscorpion](https://github.com/johneastman/Project-Eyebot/blob/master/images/enemies/Radscorpion.png)](https://fallout.fandom.com/wiki/Radscorpion_(Fallout:_New_Vegas)) | [![Bark Scorpion](https://github.com/johneastman/Project-Eyebot/blob/master/images/enemies/Scorpion.png)](https://fallout.fandom.com/wiki/Bark_scorpion) |

Feel free to click on each enemy's image to see in-game information about it.

# Image Classification
Image classification was used to train the navigation agent. Training the navigation agent also involved collecting data manually, though the process was slightly different than for the object detection model. The game was played, and each frame was mapped to a keyboard and mouse event. Below are the supported keyboard and mouse events:

| Keyboard | Mouse | Action |
|:--------:|:-----:|:------:|
| W | right | Turn right and moving forward |
| W | left  | Turn left and moving forward |
| W | none  | Moving forward |
| A | right | Turn right and moving left |
| A | left  | Turn left and moving left |
| A | none  | Moving left |
| S | right | Turn right and moving backward |
| S | left  | Turn left and moving backward |
| S | none  | Moving backward |
| D | right | Turn right and moving right |
| D | left  | Turn left and moving right |
| D | none  | Moving right |

Due to the way that the data was collected, only one keyboard-mouse event pair can be associated with a frame, meaning that this model preclude the ability to press multiple keys, for example, at once. 

# Integrating the Object Detection and Image Classification Models
After the combat and navigation models were trained, the two models were integrated into one script. At each frame of the game, the agent would first check for enemies on the screen. If an enemy was detected with a high enough score, the agent would attack the enemy. However, if no enemies were detected, the agent would use the navigation model to move around the world.

# License
This project is licensed under the [Apache License 2.0](https://github.com/johneastman/Project-Eyebot/blob/master/LICENSE).
