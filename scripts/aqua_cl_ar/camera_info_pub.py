#! /usr/bin/env python2

import rospy
from sensor_msgs.msg import CameraInfo, Image

cam_info = CameraInfo()
cam_info.height = 1200
cam_info.width = 1600
# cam_info.D = [-0.261608, 0.061877, -5.6e-05, 0.000709, 0.0]
# cam_info.K = [2*x for x in [436.21787, 0.0, 383.737445, 0.0, 436.327869, 299.754348, 0.0, 0.0, 1.0]]
# cam_info.R = [0.998602, -0.032762, 0.041483, 0.033321, 0.999362, -0.012848, -0.041035, 0.014212, 0.999057]
# cam_info.P = [2*x for x in [397.717814, 0.0, 349.338585, -36.350065, 0.0, 397.717814, 294.241598, 0.0, 0.0, 0.0, 1.0, 0.0]]

cam_info.D = [0.0, 0.0, 0.0, 0.0, 0.0]
cam_info.K = [2*569.31671203, 0.0, 2*360.09063137, 0.0, 2*569.387306625, 2*301.45327471, 0.0, 0.0, 1.0]
# cam_info.R = [0.9984530011580263, -0.05375261585017668, -0.014221841223757883, 0.05347376087546, 0.9983825171572495, -0.019310782806209553, 0.015236842729534511, 0.01852041371076275, 0.9997123750857633]
# cam_info.P = [577.8337376170499, 0.0, 358.32849884033203, -52.98629028532781, 0.0, 577.8337376170499, 311.2601547241211, 0.0, 0.0, 0.0, 1.0, 0.0]

def im_callback(msg):
    cam_info.header = msg.header
    pub.publish(cam_info)

if __name__ == "__main__":
    rospy.init_node("camera_info_pub", anonymous=True)
    pub = rospy.Publisher("camera_info", CameraInfo, queue_size=1)
    sub = rospy.Subscriber("camera_image", Image, im_callback)
    rospy.spin()
