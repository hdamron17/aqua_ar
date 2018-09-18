#! /usr/bin/env python2

import rospy
import cv_bridge
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rosbag
import sys
import rospkg

def main():
    args = ["rosbag"]
    if len(sys.argv) != len(args) + 1:
        print("Usage: extract_images_bag.py " + " ".join(args))
        return
    bag = rosbag.Bag(sys.argv[1], "r")
    bridge = CvBridge()
    img_path = rospkg.RosPack().get_path("aqua_cl_ar") + "/data/images"
    im_topic = "/cam_fr/image_raw/compressed"

    for topic, msg, bagstamp in bag.read_messages(im_topic):
        stamp = msg.header.stamp
        cv2_img = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        cv2.imwrite(img_path + "/{}.jpg".format(stamp), cv2_img)

if __name__ == "__main__":
    main()
