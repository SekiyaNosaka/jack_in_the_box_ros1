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
        self.bridge = CvBridge()
        self.rgb_img, self.d_img, self.rgbd_img = [], [], []
        self.flag_color = self.flag_depth = 0
        rospy.Subscriber('/camera/color/image_raw', Image, self.rgbImgCB)
        rospy.Subscriber('/camera/aligned_depth_to_color/image_raw', Image, self.dImgCB)

    def rgbImgCB(self, msg_color):
        try:
            self.rgb_img = self.bridge.imgmsg_to_cv2(msg_color)
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
            return 1
        except:
            return -1

    def getD(self):
        try:
            self.d_img = cv2.resize(self.d_img, dsize = (160,120))
            return 1
        except:
            return -1

    def getRGBD(self):
        try:
            self.rgbd_img = np.append(self.rgb_img, self.d_img, axis = 1)
        except:
            pass

    def main(self, save_path):
        r = rospy.Rate(3)
        n = 0
        while not rospy.is_shutdown():
            r.sleep()

            cv2.namedWindow('Realsense_Window', cv2.WINDOW_AUTOSIZE)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('j'):

                self.flag_color = self.getRGB()
                self.flag_depth = self.getD()

                if not (self.flag_color == 1 and self.flag_depth == 1):
                    continue

                print(n+1)
                print('COLOR_SHAPE: ', self.rgb_img.shape)
                print('DEPTH_SHAPE: ', self.d_img.shape)
                print('------------------------------------------')
                np.save(save_path+'/color_img' + str(n+1), self.rgb_img)
                np.save(save_path+'/depth_img' + str(n+1), self.d_img)
                n += 1

            if key == ord('f'):
                break
        cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('inference', anonymous = True)
    ts = Test()
    ts.main('~/Desktop')
