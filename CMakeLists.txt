cmake_minimum_required(VERSION 2.8.3)
project(aqua_cl_ar)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  ar_track_alvar
  geometry_msgs
  tf
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS
    roscpp
    rospy
    ar_track_alvar
    geometry_msgs
    tf
)
