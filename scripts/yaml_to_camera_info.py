#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# ROS
import rospy
from sensor_msgs.msg import Image, CameraInfo

class Yaml2CameraInfo():
    def __init__(self):
        rospy.init_node("camera_info_publisher", anonymous = True)
        # common
        self.camera_info = CameraInfo()
        self.rate = rospy.Rate(5)
        # param
        self.camera_info.width = rospy.get_param("/image_width")
        self.camera_info.height = rospy.get_param("/image_height")
        self.camera_info.distortion_model = rospy.get_param("/camera_model")
        self.camera_info.D = rospy.get_param("/distortion_coefficients/data")
        self.camera_info.K = rospy.get_param("/camera_matrix/data")
        self.camera_info.R = rospy.get_param("/rectification_matrix/data")
        self.camera_info.P = rospy.get_param("/projection_matrix/data")
        # pub
        self.camera_info_pub = rospy.Publisher("/camera_info", CameraInfo, queue_size = 1)
        # sub
        rospy.Subscriber("/texturing_image", Image, self.imageCB)
    
    def imageCB(self, msg):
        try:
            self.camera_info_pub.publish(self.camera_info)
        except:
            pass

if __name__ == "__main__":
    try:
        Yaml2CameraInfo()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
