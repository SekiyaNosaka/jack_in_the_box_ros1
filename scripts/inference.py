#!/usr/bin/env python
# -*- coding: utf-8 -*-

# General
import cv2
import numpy as np

# ROS
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Test():
	def __init__(self):
		self.rgb_img_sub = rospy.Subscriber('/camera/color/image_raw',
                                            Image, self.rgbImgCB)
		self.d_img_sub = rospy.Subscriber('/camera/aligned_depth_to_color/image_raw',
                                          Image, self.dImgCB)
		self.rgb_img, self.d_img, self.rgbd_img = [], [], []
		self.bridge = CvBridge()

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
		self.rgb_img = cv2.resize(self.rgb_img, dsize = (160,120))
		self.rgb_img = self.rgb_img.reshape(1,3,144,144)
		self.rgb_img = self.rgb_img / 255.
		return self.rgb_img

	def getD(self):
		self.d_img = cv2.resize(self.d_img, dsize = (160,120))
		self.d_img = self.d_img.reshape(1,1,144,144)
		self.d_img = self.d_img / 65535.
		return self.d_img

	def getRGBD(self):
		try:
			self.rgbd_img = np.append(self.getRGB(), self.getD(), axis = 1)
			return self.rgbd_img
		except:
			pass

if __name__ == '__main__':
	rospy.init_node('inference', anonymous = True)
	ts = Test()
	r = rospy.Rate(3)
	while not rospy.is_shutdown():
		r.sleep()
		print(ts.getRGB().shape)
