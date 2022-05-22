#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import os
import glob
import numpy as np

COLOR_NPY_PATH = '/home/sekiya/Desktop/data/color/'
DEPTH_NPY_PATH = '/home/sekiya/Desktop/data/depth/'
COLOR_PNG_PATH = '/home/sekiya/Desktop/data/color_png/'

NPY_COLOR_FILENAME = 'color_'
NPY_DEPTH_FILENAME = 'depth_'
PNG_COLOR_FILENAME = 'color_png_'

class DataAugument():
	def color_npy_horizontal_flip(self):
		color_npy_files = glob.glob(COLOR_NPY_PATH + '*.npy')
		j = 4 # color_npy元画像の全数+1
		for i in range(len(color_npy_files)):
			tmp = np.load(COLOR_NPY_PATH + NPY_COLOR_FILENAME + str(i+1) + '.npy')
			tmp_horizontal_flip = tmp[:,::-1,:]
			np.save(COLOR_NPY_PATH + NPY_COLOR_FILENAME + str(j), tmp_horizontal_flip)
			j += 1

	def depth_npy_horizontal_flip(self):
		depth_npy_files = glob.glob(DEPTH_NPY_PATH + '*.npy')
		j = 4 # depth_npy元画像の全数+1
		for i in range(len(depth_npy_files)):
			tmp = np.load(DEPTH_NPY_PATH + NPY_DEPTH_FILENAME + str(i+1) + '.npy')
			tmp_horizontal_flip = tmp[:,::-1]
			np.save(DEPTH_NPY_PATH + NPY_DEPTH_FILENAME + str(j), tmp_horizontal_flip)
			j += 1

	def color_png_horizontal_flip(self):
		color_png_files = glob.glob(COLOR_PNG_PATH + '*.png')
		j = 4 # color_png元画像の全数+1
		for i in range(len(color_png_files)):
			tmp = cv2.imread(COLOR_PNG_PATH + PNG_COLOR_FILENAME + str(i+1) + '.png')
			tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2RGB)
			tmp_horizontal_flip = tmp[:,::-1,:]
			cv2.imwrite(COLOR_PNG_PATH + PNG_COLOR_FILENAME + str(j) + '.png', tmp_horizontal_flip)
			j += 1

	def horizontal_flip(self):
		self.color_npy_horizontal_flip()
		self.depth_npy_horizontal_flip()
		self.color_png_horizontal_flip()

	def color_npy_vertical_flip(self):
		color_npy_files = glob.glob(COLOR_NPY_PATH + '*.npy')
		j = 7 # color_npy元画像の全数+1
		for i in range(len(color_npy_files)):
			tmp = np.load(COLOR_NPY_PATH + NPY_COLOR_FILENAME + str(i+1) + '.npy')
			tmp_vertical_flip = tmp[::-1,:,:]
			np.save(COLOR_NPY_PATH + NPY_COLOR_FILENAME + str(j), tmp_vertical_flip)
			j += 1

	def depth_npy_vertical_flip(self):
		depth_npy_files = glob.glob(COLOR_NPY_PATH + '*.npy')
		j = 7
		for i in range(len(depth_npy_files)):
			tmp = np.load(DEPTH_NPY_PATH + NPY_DEPTH_FILENAME + str(i+1) + '.npy')
			tmp_vertical_flip = tmp[::-1,:]
			np.save(DEPTH_NPY_PATH + NPY_DEPTH_FILENAME + str(j), tmp_vertical_flip)
			j += 1

	def color_png_vertical_flip(self):
		color_png_files = glob.glob(COLOR_PNG_PATH + '*.png')
		j = 7 # color_png元画像の全数+1
		for i in range(len(color_png_files)):
			tmp = np.load(COLOR_PNG_PATH + PNG_COLOR_FILENAME + str(i+1) + '.')
			tmp_vertical_flip = tmp[::-1,:,:]
			np.save(COLOR_NPY_PATH + NPY_COLOR_FILENAME + str(j), tmp_vertical_flip)
			j += 1

	def vertical_flip(self):
		self.color_npy_vertical_flip()
		self.depth_npy_vertical_flip()
		self.color_png_vertical_flip()

if __name__ == '__main__':
	aug = DataAugument()
	aug.vertical_flip()
