# Blur_Detection
Stream webcam/pupillometry headset data, check if video is in focus and
return a value for how blurry it is.

Created by Erin Tan and Aneesha Kodati as part of the 2020 MCA Mentorship Program, in collaboration with the Integrative Human Physiology Lab of Rutgers New Jersey Medical School

## Software Setup
- Python 3.7.4
- OpenCV 4.1.1
- ffmpeg-python (optional module to improve stream speed)
- To install module imutils:
```
pip install imutils
```

## Instructions
Open code and change variable PATH (line 10) to location of video
- Video should be of just one eye

![Headset](Images/Screen Shot 2020-09-02 at 9.11.13 AM.png)
![Pupil](Images/Screen Shot 2020-09-02 at 9.12.13 AM.png)

##### For Testing Purposes
To access user laptop webcam, set
```
PATH = 1
```

## Run Code
1. Open Command Line or Terminal Prompt
2. Navigate into Blur_Detection repository
```
cd Path/to/Blur/Detection
```
3. Use python (or python3) command to run blur_detection.py
- To run a specific .mp4 file or webcam, add argument with video address
- If no argument is added, the default is laptop webcam
```
python blur_detection.py [optional video path]
```
