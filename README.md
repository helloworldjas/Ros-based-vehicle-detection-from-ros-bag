# Ros-based-vehicle-detection-from-ros-bag
AAE4011 assignment1 question 3 
> Student Name:Lam Tsz Shun | Student ID: 25019837D | Date: 15/3/2026

---

## 1. Overview

*TThis project implements a complete ROS-based computer vision pipeline to detect vehicles from a drone camera feed. The pipeline extracts frames from a provided `.bag` file, processes them using a deep learning model, and visualizes the bounding boxes, class labels, and confidence scores in a continuous UI.
 *

## 2. Detection Method *(Q3.1 — 2 marks)*

*For this project, I selected the **YOLOv8 Nano (`yolov8n.pt`)** object detection model. YOLOv8 was chosen because of its exceptional balance between speed and accuracy, which is critical for real-time video processing. Because the model is lightweight, it can process the rosbag video feed smoothly without requiring high-end GPU hardware, while still accurately identifying standard vehicle classes (cars, buses, motorcycles, and trucks) from the COCO dataset.*

## 3. Repository Structure
```text
catkin_ws/src/vehicle_detection/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── pipeline.launch           # Launch file to run the entire project
├── scripts/
│   ├── bag_extractor.py          # Script for Q3.1 image extraction requirement
│   └── single_pipeline_ui.py        # Main Python script for detection and UI
└── data/
    └── [Your_Rosbag_File].bag    # Place the rosbag here
```
## 4. Prerequisites

OS: Ubuntu 20.04

ROS Version: ROS Noetic

Python Version: Python 3.8+

Key Libraries: rospy, sensor_msgs, cv_bridge, opencv-python (cv2), rosbag, ultralytics (YOLO)

## 5. How to Run *(Q3.1 — 2 marks)*

*Provide clear, step-by-step instructions:*

1. Clone the repository and setup workspace
```text
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone [Your-GitHub-Repository-Link] vehicle_detection
```

2. Build the ROS package
```text
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

3. Install Python dependencies
```text
pip3 install opencv-python ultralytics matplotlib numpy
```

4. Make Scripts Executable
```text
chmod +x ~/aae4011_ws/src/vehicle_detection/scripts/single_pipeline.py
chmod +x ~/aae4011_ws/src/vehicle_detection/scripts/bag_extractor.py
```
5.Prepare the Rosbag Data

lace the provided .bag file into the data/ folder. Open single_pipeline.py and ensure the bag_file and topic_name variables match your specific rosbag file.
```text
rosbag info [directry of the bag].bag    #To check the Rosbag info for the pipeline to launch 
```

6. Launch the pipeline<br>
Start a ROS core and run the pipeline node directly. Note: Ensure your rosbag path inside single_pipeline.py is updated to point to your local .bag file.
```text
cd ~/catkin_ws/src/vehicle_detection/scripts
python3 single_pipeline.py
```
## 6. Sample Results
sample screen<br>
<img width="3004" height="1973" alt="Advanced Vehicle Detection UI_screenshot_16 03 2026" src="https://github.com/user-attachments/assets/a3b35d76-b899-45f3-9962-2fc56b375c7b" />
summery/result of the rosbag<br> 
<img width="2126" height="1051" alt="image" src="https://github.com/user-attachments/assets/ddd5ade8-7f6f-4ab1-a563-45bd5c3183a2" />

## 7. Video Demonstration *(Q3.2 — 5 marks)*

**Video Link:** [YouTube (Unlisted)](https://youtu.be/JFdefZvHPwU)


## 8. Reflection & Critical Analysis *(Q3.3 — 8 marks, 300–500 words)*

### (a) What Did You Learn? *(2 marks)*

during the process of this assignment i learned how to manage ROS message types, specifically converting messages into usable OpenCV arrays. I also learned how to build a complex structure programme managed with some AI agent. The AI agent also help me to debug or solve the problem that appear during constructing the whole Ros enviroment. While follow the step from AI i also learn skills to read the python code and the ROS structure need in this assignment. In the final stage writing readme recab the memory to writing the markdown format file.

### (b) How Did You Use AI Tools? *(2 marks)*

i used gemini to guide me setup the ROS environment and the ROSbag strcture.it also  helped me diagnose a  error caused by Windows line endings, and it provided the mathematical approach (cv2.copyMakeBorder) needed to append a clean, non-overlapping side panel to my OpenCV video window Then i used antigravity with claude to help my coding part which is the UI architecture, debug coding errors and design the python code of the single launch pipline programme. The limitation of using AI in this assignment is the AI agent will limit the output or hallucinate due to context window is small as it will forget the requirement i set in the beginning part of the prompt or the setting set itself. so setting up agent skill for the AI agent is important to reduce the token use during the AI is reading the context.

### (c) How to Improve Accuracy? *(2 marks)*

1. Lowering the Confidence Threshold, that will increase the sensitivity. As YOLO discards detections below a 25% confidence score. Lowering this threshold to helps the model identify distant or partially obscured vehicles that lack clear distinguishing features.<br>

2. Increasing Inference Resolution YOLOv8 downscales images to 640x640 before processing. By forcing the model to process at a higher resolution using the "imgsz=1280" parameter,distant vehicles retain more pixel density, making them significantly easier for the neural network to detect

### (d) Real-World Challenges *(2 marks)*

1. Computational Limitations: Running deep learning models like YOLOv8 on an actual drone's companion computer like a Raspberry Pi is computationally expensive.This can severely drop the frames per second , leading to processing latency that could cause the drone to react too slowly to dynamic obstacles in real time.

2. Variable Lighting and Weather real-world drone cameras are exposed to extreme glare, harsh shadows, rain, and low-light conditions. The high noise from raw data and mist will highly affect the accuracy of the detection to surrounding. 

## 9. References

Ultralytics YOLOv8 Documentation: https://docs.ultralytics.com/

ROS Noetic cv_bridge Tutorial: http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

cv_bridge Tutorials: http://wiki.ros.org/cv_bridge

OpenCV Documentation: https://docs.opencv.org/
