#! /usr/bin/env python2

import rospy
from sensor_msgs.msg import Image
import cv_bridge
import cv2
from cv_bridge import CvBridge, CvBridgeError

def save_image(msg):
    stamp = msg.header.stamp
    cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imwrite(img_path + "/{}.jpg".format(stamp), cv2_img)

if __name__ == "__main__":
    bridge = CvBridge()

    rospy.init_node('extract_images', anonymous=True)
    img_path = rospy.get_param("~image_dir", ".")
    sub = rospy.Subscriber("camera_image", Image, save_image)
    rospy.spin()
