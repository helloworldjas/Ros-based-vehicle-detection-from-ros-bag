#!/usr/bin/env python3
import os
os.environ['QT_LOGGING_RULES'] = 'qt.qpa.*=false'  # Silence OpenCV terminal warnings

import rosbag
import cv2
import numpy as np
from cv_bridge import CvBridge
from ultralytics import YOLO
import matplotlib.pyplot as plt

def detect_and_draw(cv_image, model):
    """Runs YOLOv8 and draws boxes, center points, and position stats."""
    results = model(cv_image, verbose=False, device='cpu') 
    vehicle_classes = [2, 3, 5, 7] # COCO IDs: car, motorcycle, bus, truck
    
    v_count = 0
    detections_list = []
    
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            if cls_id in vehicle_classes:
                v_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                class_name = model.names[cls_id].capitalize()
                
                # Center coordinates
                cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
                
                # Format for the right-hand panel
                detections_list.append(f"{class_name} | {conf:.2f} | Pos: ({cx},{cy})")
                
                # Draw Box and Center Dot
                cv2.rectangle(cv_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(cv_image, (cx, cy), 5, (0, 0, 255), -1)
                
                # Draw Info on TOP of the bounding box
                # max(15, y1-10) ensures text doesn't go off the top of the screen
                label = f"{class_name} {conf:.2f} Pos:({cx},{cy})"
                cv2.putText(cv_image, label, (x1, max(15, y1 - 10)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
    return cv_image, v_count, detections_list

def main():
    # UPDATE THESE PATHS
    bag_file = '/home/jason/catkin_ws/src/vehicle_detection/data/assignment2.bag' 
    topic_name = '/hikcamera/image_1/compressed'
    
    print("Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt')
    bridge = CvBridge()
    
    # 1. Pre-load messages into a list to allow random seeking
    print("Extracting rosbag to memory for random-access playback...")
    bag = rosbag.Bag(bag_file, 'r')
    messages = [msg for _, msg, _ in bag.read_messages(topics=[topic_name])]
    bag.close()
    
    total_frames = len(messages)
    if total_frames == 0:
        print(f"Error: 0 frames found for '{topic_name}'. Check topic name!")
        return

    # Extract resolution from the very first frame
    try:
        first_frame = bridge.compressed_imgmsg_to_cv2(messages[0], "bgr8")
    except AttributeError:
        first_frame = bridge.imgmsg_to_cv2(messages[0], "bgr8")
    img_h, img_w = first_frame.shape[:2]
    resolution_str = f"{img_w} x {img_h}"
    
    # --- Setup UI Window ---
    window_name = "Advanced Vehicle Detection UI"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1400, img_h + 100) # Give extra width for the panel
    
    current_frame_index = 0
    is_paused = False
    
    # Trackbar callback function
    def on_trackbar(val):
        nonlocal current_frame_index
        current_frame_index = min(val, total_frames - 1)
        
    cv2.createTrackbar('Progress', window_name, 0, total_frames - 1, on_trackbar)
    
    # Array to track vehicle counts per frame for the final graph
    # (Using an array so if the user scrubs, we record data accurately at the right index)
    graph_data = [None] * total_frames 

    print("Playback ready. Press 'Spacebar' to Play/Pause, 'q' to Quit.")
    
    try:
        while True:
            # Get specific frame from our pre-loaded list
            msg = messages[current_frame_index]
            try:
                cv_image = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="bgr8")
            except AttributeError:
                cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
                
            # Run Detection
            processed_img, v_count, det_list = detect_and_draw(cv_image, model)
            graph_data[current_frame_index] = v_count # Save for final graph
            
            # --- Build the UI Canvas (Add Right Panel) ---
            panel_width = 450
            # Pad the image with a dark gray block on the right
            canvas = cv2.copyMakeBorder(processed_img, 0, 0, 0, panel_width, 
                                        cv2.BORDER_CONSTANT, value=(40, 40, 40))
            
            # Text layout settings
            text_x = img_w + 20
            
            # Block 1: Extraction Summary
            cv2.putText(canvas, "--- EXTRACTION SUMMARY ---", (text_x, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(canvas, f"Topic: {topic_name}", (text_x, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
            cv2.putText(canvas, f"Resolution: {resolution_str}", (text_x, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
            cv2.putText(canvas, f"Total Frames: {total_frames}", (text_x, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)
            cv2.putText(canvas, f"Current Frame: {current_frame_index} / {total_frames-1}", (text_x, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 1)
            
            # Playback Status
            status_txt = "PAUSED" if is_paused else "PLAYING"
            cv2.putText(canvas, f"Status: {status_txt} (Space to toggle)", (text_x, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 165, 255), 2)
            
            # Block 2: Detection List
            cv2.putText(canvas, "--- CURRENT DETECTIONS ---", (text_x, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(canvas, f"Vehicles in Frame: {v_count}", (text_x, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Print list of vehicles dynamically
            y_offset = 350
            for i, item in enumerate(det_list):
                cv2.putText(canvas, f"{i+1}. {item}", (text_x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += 30
                
            cv2.imshow(window_name, canvas)
            
            # Advance video if playing
            if not is_paused:
                if current_frame_index < total_frames - 1:
                    current_frame_index += 1
                    cv2.setTrackbarPos('Progress', window_name, current_frame_index)
                else:
                    is_paused = True # Auto-pause at the end of the video
            
            # Controls
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q'):
                break
            elif key == ord(' '):
                is_paused = not is_paused
                
    finally:
        cv2.destroyAllWindows()
        
    # --- Generate Post-Video Summary and Graph ---
    print("\nProcessing final data summary...")
    
    # Filter out frames the user might have skipped while scrubbing
    processed_indices = [i for i, v in enumerate(graph_data) if v is not None]
    processed_counts = [v for v in graph_data if v is not None]
    
    if processed_counts:
        plt.figure(figsize=(10, 5))
        plt.plot(processed_indices, processed_counts, color='royalblue', linewidth=2, label='Vehicles Detected')
        plt.fill_between(processed_indices, processed_counts, color='royalblue', alpha=0.2)
        plt.title('Vehicle Detection Frequency')
        plt.xlabel('Frame Number')
        plt.ylabel('Total Vehicles')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig('detection_summary_graph.png')
        print("Graph saved as 'detection_summary_graph.png'. Close the plot to exit script.")
        plt.show()

if __name__ == '__main__':
    main()
