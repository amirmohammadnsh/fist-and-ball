# fist-and-ball
Fist&amp;Ball is a rehabilitation exercise game developed in Blender. Patients who suffer from hand amputees practice fist gestures with the help of magnets implanted in their forearms.
# Notes
- The *Fist-and-Ball* add-on consists of a virtual left hand, an orange ball and nine LEDs. The [3D-Hand model](https://blendswap.com/blend/22357) by *[cgcookie](https://blendswap.com/profile/8267)* was used to build a rigged-hand by using armatures as the bones of each finger. Also, the"Copy Constraints" and "Inverse Kinematics" add-ons of Blender was used to ease the visualization of hand gestures. The orange ball will be moving in up and down directions. The patient will practice performing a fist gesture by capturing and holding the orange ball. The nine LEDs indicate the stages between open palm and closed fist.
- This add-on is compatible with both Blender 2.83 LTS and 2.93 LTS versions (**Windows**)
# Usage
**Set Blender to *run as an administrator* by default.**
1. It is required to add Scipy package compatible to the python enviroment version of your Blender.
  - Add it manually to your site-packages folder of your Blender, which is "**Installation Directory\Blender Foundation\Blender 2.93\2.93\python\lib\site-packages**"
  - Use [2nd method](https://stackoverflow.com/questions/11161901/how-to-install-python-modules-in-blender) 
2. Place all listed modules to  "**Installation Directory\Blender Foundation\Blender 2.93\2.93\scripts\modules**"
  - **deviceConnection** 
  - **fistAndBall_modal_timer_operator**
  - **fistAndBall_ui_panel**
  - **hand_logic**
  - **hand_visualization**
  - **implantedMagnets**
  - **leds**
  - **sampleLogger**
  - **sceneObjects**
  - **upperLimb**
3. In our project, we exploit calibrated data of magnetometers. Therefore, the address of calibrationParams folder should be set by **calibPath** variable in the **modalTimerOperator.py**. Also, number of magnetometers, deivce ip and port should be set in this file.
4. Import *.blend* file to Blender.
5. From **Edit/Preferences/Add-ons**, install *main.py*, then activate it.
6. By pressing *"N"* shortcut key inside blender, you can view the add-on ui panel.
7. The sampled data and the patient's progress will be saved in the *Fist&Ball-Log-Files* foler in "**Installation Directory\Blender Foundation\Blender 2.93**".
# Game Environment
![alt text](https://github.com/amirmohammadnsh/fist-and-ball/blob/main/env.jpg)
# Add-On Panel UI
![alt text](https://github.com/amirmohammadnsh/fist-and-ball/blob/main/panel_ui.jpg)
# Gameplay
https://user-images.githubusercontent.com/28790347/181814953-f27285db-462f-4ef3-b268-3c9a06a71abd.mp4
# Paper
This is the implementation of the **Fist and Ball** game mentioned in our paper titled [**Clinical implementation of a bionic hand controlled with kineticomyographic signals**](https://www.nature.com/articles/s41598-022-19128-1). If this work or paper is useful for your research, please cite our paper:
```
@article{
  title={Clinical implementation of a bionic hand controlled with kineticomyographic signals},
  author = {Ali Moradi, Hamed Rafiei, Mahla Daliri, Mohammad-R. Akbarzadeh-T., Alireza Akbarzadeh, Amir-M. Naddaf-Sh and Sadra Naddaf-Sh},
  doi = {10.1038/s41598-022-19128-1},
  url = {https://doi.org/10.1038/s41598-022-19128-1},
  journal = {Scientific Reports},
  year = {2022}
}
```


