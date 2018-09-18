Small package to get AR tags and transform into pose of second AQUA for Deep CL project.

To run, simply `roslaunch aqua_cl_ar ar_pose.launch`

Assumes topic /cam_$(arg cam)/image_raw is present.

Provides a static /cam_$(arg cam)/camera_info; remove camera_info_pub node from launch file if not needed.
Transports image from compressed to raw, but this too can be changed in the launch file.

To change the transform from AR tag to base, change ar_to_base variable in ar_pose_transformer.py
