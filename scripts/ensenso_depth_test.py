#!/usr/bin/env python

# General
import cv2
import numpy as np

# ROS
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Test():
    def __init__(self):
        self.bridge = CvBridge()
        rospy.Subscriber('/depth/image',
                Image,
                self.dImgCB,)

    def dImgCB(self, msg):
        try:
            self.d_img = self.bridge.imgmsg_to_cv2(msg)
            print(self.d_img.shape)
            np.save('./depth.npy', self.d_img)
            cv2.imwrite('./depth.png', self.d_img)
        except CvBridgeError as error:
            print(error)

if __name__ == '__main__':
    rospy.init_node('inference', anonymous = True)
    t = Test()
    rospy.spin()
