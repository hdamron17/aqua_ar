#! /usr/bin/env python2

import rospy
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
    img_path = rospkg.RosPack().get_path("aqua_cl_ar") + "/data/images"
    im_topic = "/cam_fr/image_raw/compressed"
    if out_file.endswith("gz"):
        compress = "gz"
    elif out_file.endswith("bz2"):
        compress = "bz2"
    else:
        compress = ""
    im_tarfile = tarfile.open(out_file, "w:{}".format(compress))

    for topic, msg, bagstamp in bag.read_messages(im_topic):
        stamp = msg.header.stamp
        if "jpeg" in msg.format:
            fmt = "jpeg"
        elif "png" in msg.format:
            fmt = "png"
        else:
            fmt = "raw"
        im_info = tarfile.TarInfo("{}.{}".format(stamp, fmt))
        im_info.size = len(msg.data)
        im_tarfile.addfile(im_info, io.BytesIO(msg.data))

if __name__ == "__main__":
    main()
