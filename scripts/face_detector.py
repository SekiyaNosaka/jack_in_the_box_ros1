#!/usr/bin/env python

# General
import time
import math
import cv2
import numpy as np

# ROS
import rospy

class humanObjectDetection:
    def __init__(self):
        self.cap = cv2.VideoCapture(7)
        self.casc = cv2.CascadeClassifier("./cascade_weight/haarcascade_frontalface_alt.xml")
        self.human_detection_count = 0
        self.human_event_count = 0

    def humanDetection(self):
        while(True):
            self.ret, self.frame = self.cap.read()
            self.facerect = self.casc.detectMultiScale(self.frame,
                                                       scaleFactor = 1.2,
                                                       minNeighbors = 2,
                                                       minSize = (1, 1))
            if type(self.facerect) == np.ndarray:
                self.human_detection_count += 1
                print("facerect: " + str(self.facerect))
                print("human_detection_count: " + str(self.human_detection_count) + "\n")
                # print(self.frame)

            for rect in self.facerect:
                cv2.rectangle(self.frame,
                              tuple(rect[0:2]),
                              tuple(rect[0:2] + rect[2:4]),
                              (255, 0, 0),
                              thickness = 3)
                self.text = 'Person_face'
                self.font = cv2.FONT_HERSHEY_PLAIN
                cv2.putText(self.frame,
                            self.text,
                            (rect[0], rect[1]-10),
                            self.font, 2, (255, 255, 255),
                            3, cv2.LINE_AA)

            cv2.imshow("Show FLAME Image", self.frame)

            self.k = cv2.waitKey(1)
            if self.k == ord("q") or self.human_detection_count == 100:
                self.human_detection_count = 0
                self.human_event_count += 1
                # print(self.frame.shape)
                # self.frame = self.frame[None, :, :, :]
                # cv2.imwrite("./face_generate_img/face_sample" + str(self.human_event_count)+ ".jpg", self.frame)
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    rospy.init_node("face_detect")
    hod = humanObjectDetection()
    hod.humanDetection()
