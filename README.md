# Project Eyebot
Project Eyebot is an artificial agent that plays [Fallout: New Vegas](https://fallout.fandom.com/wiki/Fallout:_New_Vegas). This project was designed and developed by [Caitlin Chapdelaine](https://www.linkedin.com/in/caitlin-chapdelaine-5a625516b/) and [John Eastman](https://www.linkedin.com/in/john-eastman-80a352136/) and was their [Champlain College](https://www.champlain.edu/) Senior project.

# Object Detection
Object detection was used for the combat agent. This entailed training an object-detection model on what enemies look like. Data for the object-detection model was collected by screen capturing the game as it was played. The data was then labeled manually using [LabelImg](https://github.com/tzutalin/labelImg) and trained using the Faster RCNN Inception V2 COCO model. 

For the purpose of this project, the object-detection model was trained on the following enemies:

| Enemy Name | Enemy Image |
|------------|--------------
| Bloatfly   | ![Bloatfly](https://github.com/johneastman/Project-Eyebot/blob/master/images/enemies/Bloatfly.png){:height="50%" width="50%"} |


# Image Classification
Image classification was used to train the navigation agent.

# License
This project is licensed under the [Apache License 2.0](https://github.com/johneastman/Project-Eyebot/blob/master/LICENSE).
