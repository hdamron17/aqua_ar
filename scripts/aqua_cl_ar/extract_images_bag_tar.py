#! /usr/bin/env python2

import rospy
import cv_bridge
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rosbag
import sys
import rospkg
import tarfile
import io

def main():
    args = ["rosbag", "outfile"]
    if len(sys.argv) != len(args) + 1:
        print("Usage: extract_images_bag.py " + " ".join(args))
        return
    bag_filename, out_file = sys.argv[1:3]
    bag = rosbag.Bag(bag_filename, "r")
    bridge = CvBridge()
    img_path = rospkg.RosPack().get_path("aqua_cl_ar") + "/data/images"
    im_topic = "/cam_fr/image_raw/compressed"
    im_tarfile = tarfile.open(out_file, "w")

    for topic, msg, bagstamp in bag.read_messages(im_topic):
        stamp = msg.header.stamp
        cv2_img = bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        success, buf = cv2.imencode(".jpg", cv2_img)
        im_info = tarfile.TarInfo("{}.jpg".format(stamp))
        im_info.size = len(buf)
        im_tarfile.addfile(im_info, io.BytesIO(buf.tobytes()))

if __name__ == "__main__":
    main()
