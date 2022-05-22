#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################
# RealSense D435i RGB-D save (npy)
#
# COLOR_FRAME: 1920 * 1080 (* 3)
# DEPTH_FRAME: 1280 * 720  (* 1)
######################################

# General
import os
import glob
import cv2
import numpy as np
import pyrealsense2 as rs

def config_pyrealsense():
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) #  8bit
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16,  30) # 16bit

    pipeline = rs.pipeline()
    profile = pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)
	return pipeline, align

def color_resize_and_normalization(color_frame): # output: (120,160,3)
    color_image = np.array(color_frame.get_data())
    #color_image = cv2.resize(color_image, dsize = (160,120))
    #color_image = color_image[:,:,::-1]
    #color_image = color_image / 255.
    return color_image

def depth_resize_and_normalization(depth_frame): # output: (120,160)
    depth_image = np.array(depth_frame.get_data())
    #depth_image = cv2.resize(depth_image, dsize = (160,120))
    #depth_image = depth_image / 65535.
    return depth_image

def depth_coloring(depth_coloring_frame):
    depth_coloring_image = np.array(depth_coloring_frame.get_data())
    #depth_coloring_image = cv2.resize(depth_coloring_image, dsize = (160,120))
    return depth_coloring_image

def save_RGB_D_image_from_key():
    pipeline, align = config_pyrealsense()
    n = 0
    while True:
        # wait for a frame(Color & Depth)
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()
        depth_coloring_frame = rs.colorizer().colorize(depth_frame)

        # RGB (HEIGHT,WIDTH,3) & normalization
        color_image = color_resize_and_normalization(color_frame)
        # D (HEIGHT,WIDTH) & normalization
        depth_image = depth_resize_and_normalization(depth_frame)
        # D_coloring (HEIGHT,WIDTH,3)
        depth_coloring_image = depth_coloring(depth_coloring_frame)
        #drawing_images = np.hstack((color_image[:,:,::-1], depth_coloring_image))
        drawing_images = np.hstack((color_image, depth_coloring_image))

        cv2.imshow('RGB-D_frame', drawing_images)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('j'):
            cv2.imwrite('/home/sekiya/Desktop/data/color_png/color_png_' + str(n+1) + '.png', color_image)
            cv2.imwrite('/home/sekiya/Desktop/data/depth_png/depth_png_' + str(n+1) + '.png', depth_image)
            np.save('/home/sekiya/Desktop/data/color_npy/color_npy_' + str(n+1), cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
            np.save('/home/sekiya/Desktop/data/depth_npy/depth_npy_' + str(n+1), depth_image)	
            n += 1
        if key == ord('f'):
            break
    pipeline.stop()
    cv2.destroyAllWindows()

def mkdir():
    if not os.path.exists('/home/sekiya/Desktop/data'):
        os.mkdir('/home/sekiya/Desktop/data')
    if not os.path.exists('/home/sekiya/Desktop/data/color_npy') or not os.path.exists('/home/sekiya/Desktop/data/depth_npy'):
        os.mkdir('/home/sekiya/Desktop/data/color_npy')
        os.mkdir('/home/sekiya/Desktop/data/depth_npy')
    if not os.path.exists('/home/sekiya/Desktop/data/color_png') or not os.path.exists('/home/sekiya/Desktop/data/depth_png'):
        os.mkdir('/home/sekiya/Desktop/data/color_png')
        os.mkdir('/home/sekiya/Desktop/data/depth_png')

if __name__ == '__main__':
    mkdir()
    save_RGB_D_image_from_key() # save RGB-D img(npy & png format)
