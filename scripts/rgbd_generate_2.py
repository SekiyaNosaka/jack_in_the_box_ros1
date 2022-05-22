#!/usr/bin/env python

# General
import os
import cv2
import numpy as np

# ROS
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Test():
    def __init__(self):
        self.rgb_resize_pub = rospy.Publisher('/camera_resize' , Image, queue_size = 10)
        rospy.Subscriber('/camera/color/image_raw', Image, self.rgbImgCB)
        rospy.Subscriber('/camera/aligned_depth_to_color/image_raw',
                         Image, self.dImgCB)
        self.bridge = CvBridge()
        self.rgb_img, self.d_img, self.rgbd_img = [], [], []
        self.flag_color = self.flag_depth = 0

    def rgbImgCB(self, msg_color):
        try:
            self.rgb_img = self.bridge.imgmsg_to_cv2(msg_color)
            print(self.rgb_img.shape)
        except CvBridgeError as error_msg:
            print(error_msg)

    def dImgCB(self, msg_depth):
        try:
            self.d_img = self.bridge.imgmsg_to_cv2(msg_depth)
        except CvBridgeError as error_msg:
            print(error_msg)

    def getRGB(self):
        try:
            self.rgb_img = cv2.resize(self.rgb_img, dsize = (160,120))
            self.rgb_pub = cv2.cvtColor(self.rgb_img, cv2.COLOR_BGR2RGB)
            #self.rgb_img = cv2.cvtColor(self.rgb_img, cv2.COLOR_BGR2RGB)
            #self.rgb_img = self.rgb_img.reshape(1,3,120,160)
            #self.rgb_img = self.rgb_img / 255.
            self.rgb_pub = self.bridge.cv2_to_imgmsg(self.rgb_img)
            self.rgb_resize_pub.publish(self.rgb_pub)
        except:
            pass

    def getD(self):
        try:
            self.d_img = cv2.resize(self.d_img, dsize = (160,120))
            #self.d_img = self.d_img.reshape(1,1,120,160)
            #self.d_img = self.d_img / 65535.
        except:
            pass

    def getRGBD(self):
        try:
            self.rgbd_img = np.append(self.getRGB(), self.getD(), axis = 1)
        except:
            pass

    def main(self):
        r = rospy.Rate(3)
        n = 0

        while not rospy.is_shutdown():
            r.sleep()
            self.getRGB()
            print(self.rgb_img.shape)
            print('------------*------------')
            print('------------*------------')
            if n == 10:
                break
            n += 1

if __name__ == '__main__':
    rospy.init_node('inference', anonymous = True)
    ts = Test()
    r = rospy.Rate(3)
    while not rospy.is_shutdown():	
        r.sleep()
        ts.getRGB()
