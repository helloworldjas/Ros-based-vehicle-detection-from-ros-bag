# Ros-based-vehicle-detection-from-ros-bag
AAE4011 assignment1 question 3 
> **Student Name:Lam Tsz Shun | **Student ID:** 25019837D | **Date:** 15/3/2026

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
│   └── single_pipeline.py        # Main Python script for detection and UI
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
2. Install Python dependencies
```text
pip3 install opencv-python ultralytics
```
3. Build the ROS package
```text
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```
4. Place the rosbag file
```text
chmod +x ~/aae4011_ws/src/vehicle_detection/scripts/single_pipeline.py
chmod +x ~/aae4011_ws/src/vehicle_detection/scripts/bag_extractor.py
```
6. Launch the pipeline<br>
Start a ROS core and run the pipeline node directly. Note: Ensure your rosbag path inside single_pipeline.py is updated to point to your local .bag file.
```text
roscore &
rosrun vehicle_detection single_pipeline.py
```
## 6. Sample Results

*Include:*
- Image extraction summary (total frames, resolution, topic name)
- Detection results (sample screenshot, detection statistics)

## 7. Video Demonstration *(Q3.2 — 5 marks)*

**Video Link:** [YouTube (Unlisted)](https://youtu.be/your-link-here)

*The video (1–3 min) should show:*
- (a) Launching the ROS package
- (b) The UI displaying detection results
- (c) A brief explanation of the results

## 8. Reflection & Critical Analysis *(Q3.3 — 8 marks, 300–500 words)*

### (a) What Did You Learn? *(2 marks)*

*Identify at least two specific technical skills or concepts you gained.*

### (b) How Did You Use AI Tools? *(2 marks)*

*Describe how you used AI assistants. Discuss both benefits and limitations. If you did not use any, explain your alternative approach.*

### (c) How to Improve Accuracy? *(2 marks)*

*Propose two concrete strategies to improve detection accuracy and explain why each would help.*

### (d) Real-World Challenges *(2 marks)*

*Discuss two challenges of deploying this pipeline on an actual drone in real time.*

## 9. References

Ultralytics YOLOv8 Documentation: https://docs.ultralytics.com/

ROS Noetic cv_bridge Tutorial: http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
