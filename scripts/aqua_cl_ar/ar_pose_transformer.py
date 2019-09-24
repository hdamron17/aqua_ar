#! /usr/bin/env python2

import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import PoseStamped, Pose
import tf
import tf.transformations as pytf
import numpy as np
from math import pi
import os, os.path
import time
import csv

ar_to_base = ([0, -(0.125/5 + 0.044 - 0.004 + 0.126/2)-0.03, 0.49/2 - 0.02], pytf.quaternion_from_euler(0, 93*pi/180, pi/2))

def msg2tf(msg):
    p, q = msg.position, msg.orientation
    return np.array([p.x, p.y, p.z]), np.array([q.x, q.y, q.z, q.w])

def tf2msg(pose):
    msg = Pose()
    msg.position.x, msg.position.y, msg.position.z = pose[0]
    msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w = pose[1]
    return msg

def applyTransform(tfl, tfr):
    tfl_mat = pytf.quaternion_matrix(tfl[1])
    tfl_mat[:3,3] = tfl[0]
    out_tf = np.matmul(tfl_mat, np.append(tfr[0], [1]))[:3], pytf.quaternion_multiply(tfl[1], tfr[1])
    return out_tf

def ar_callback(msg):
    markers = msg.markers
    if target_id >= 0:
        markers = filter(lambda m: m.id == target_id, markers)
    if len(markers) > 0:
        marker = next(iter(markers))
        pose = marker.pose
        pose.header = marker.header
        pose_tf = msg2tf(pose.pose)
        pose_tf = applyTransform(pose_tf, ar_to_base)
        pose.pose = tf2msg(pose_tf)
        br.sendTransform(ar_to_base[0], ar_to_base[1], pose.header.stamp, "aqua2", "ar_marker_%d" % marker.id)
        br.sendTransform(pose_tf[0], pose_tf[1], pose.header.stamp, "aqua2_alt", pose.header.frame_id)
        csv_writer.writerow([pose.header.stamp] + pose_tf[0].tolist() + pose_tf[1].tolist())
        pub.publish(pose)

def close_csv():
    csv_file.close()

if __name__ == "__main__":
    rospy.init_node("ar_pose_transformer", anonymous=True)
    target_id = rospy.get_param("~id", -1)
    br = tf.TransformBroadcaster()
    filename = "ar_marker_%d_%s.csv" % (target_id, time.strftime("%Y-%m-%d-%H-%M-%S"))
    csv_file = open(os.path.join(rospy.get_param("~csv_dir", "."), filename), "w+")
    csv_writer = csv.writer(csv_file, delimiter=",")
    csv_writer.writerow(["stamp", "pos.x", "pos.y", "pos.z", "rot.x", "rot.y", "rot.z", "rot.w"])
    rospy.on_shutdown(close_csv)
    pub = rospy.Publisher("aqua_pose", PoseStamped, queue_size=1)
    sub = rospy.Subscriber("ar_pose_marker", AlvarMarkers, ar_callback)
    rospy.spin()
