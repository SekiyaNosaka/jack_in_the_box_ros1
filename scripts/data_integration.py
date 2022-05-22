#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import numpy as np

COLOR_NPY_PATH = '/home/sekiya/Desktop/data/color/'
DEPTH_NPY_PATH = '/home/sekiya/Desktop/data/depth/'
INTEGRA_NPY_PATH = '/home/sekiya/Desktop/data/integra/'

NPY_COLOR_FILENAME = 'color_'
NPY_DEPTH_FILENAME = 'depth_'
NPY_INTEGRA_COLOR_FILENAME = 'integration_color'
NPY_INTEGRA_DEPTH_FILENAME = 'integration_depth'
NPY_INTEGRA_RGBD_FILENAME = 'integration_rgbd'

class Integration():
	def __init__(self):
		#self.color_integration_npy = np.zeros((1,144,144,3)) # keras仕様
		#self.depth_integration_npy = np.zeros((1,144,144,1)) # keras仕様
		self.color_integration_npy = np.zeros((1,3,144,144)) # Pytorch仕様
		self.depth_integration_npy = np.zeros((1,1,144,144)) # Pytorch仕様
		self.rgbd_integration_npy = 0
		if not os.path.exists(INTEGRA_NPY_PATH):
			os.mkdir(INTEGRA_NPY_PATH)

	def color_npy_integration(self): # RGBだけで全画像枚数をintegration
		color_npy_files = glob.glob(COLOR_NPY_PATH + '*.npy')
		for i in range(len(color_npy_files)):
			tmp = np.load(COLOR_NPY_PATH + NPY_COLOR_FILENAME + str(i+1) + '.npy') # (144,144,3)
			#tmp = tmp.reshape(1,144,144,3) # keras仕様
			tmp = tmp.reshape(1,3,144,144) # Pytorch仕様
			self.color_integration_npy = np.append(self.color_integration_npy, tmp, axis = 0)

		self.color_integration_npy = np.delete(self.color_integration_npy, 0, axis = 0)
		np.save(INTEGRA_NPY_PATH + NPY_INTEGRA_COLOR_FILENAME, self.color_integration_npy)

	def depth_npy_integration(self): # Dだけで全画像枚数をintegration
		depth_npy_files = glob.glob(DEPTH_NPY_PATH + '*.npy')
		for i in range(len(depth_npy_files)):
			tmp = np.load(DEPTH_NPY_PATH + NPY_DEPTH_FILENAME + str(i+1) + '.npy') # (144,144,1)
			#tmp = tmp.reshape(1,144,144,1) # keras仕様
			tmp = tmp.reshape(1,1,144,144) # Pytorch仕様
			self.depth_integration_npy = np.append(self.depth_integration_npy, tmp, axis = 0)

		self.depth_integration_npy = np.delete(self.depth_integration_npy, 0, axis = 0)
		np.save(INTEGRA_NPY_PATH + NPY_INTEGRA_DEPTH_FILENAME, self.depth_integration_npy)

	def rgbd_npy_integration(self): # RGB-Dで全画像枚数をintegration (color_npy_integrationとdepth_npy_integration実行後で可能)
		color_npy_integration = np.load(INTEGRA_NPY_PATH + NPY_INTEGRA_COLOR_FILENAME + '.npy')
		depth_npy_integration = np.load(INTEGRA_NPY_PATH + NPY_INTEGRA_DEPTH_FILENAME + '.npy')
		self.rgbd_integration_npy = np.concatenate([color_npy_integration, depth_npy_integration], axis = 1)
		np.save(INTEGRA_NPY_PATH + NPY_INTEGRA_RGBD_FILENAME, self.rgbd_integration_npy)

	def main(self):
		self.color_npy_integration()
		self.depth_npy_integration()
		self.rgbd_npy_integration()

if __name__ == '__main__':
	itg = Integration()
	itg.main()
