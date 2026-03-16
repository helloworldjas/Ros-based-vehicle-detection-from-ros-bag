import rosbag
import cv2
from cv_bridge import CvBridge

bag_file = 'your_provided_file.bag'
topic_name = '/camera/image_raw' # Adjust to match your bag

bag = rosbag.Bag(bag_file, 'r')
bridge = CvBridge()
count = 0

for topic, msg, t in bag.read_messages(topics=[topic_name]):
    cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    cv2.imwrite(f"extracted_frames/frame_{count:04d}.jpg", cv_img)
    count += 1

print(f"Extraction complete. Total images extracted: {count}")
bag.close()
