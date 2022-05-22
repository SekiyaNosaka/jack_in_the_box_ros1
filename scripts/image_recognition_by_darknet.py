#!/usr/bin/env python
# -*- coding: utf-8 -*-

# General
import time

# ROS
import rospy
from darknet_ros_msgs.msg import BoundingBox, BoundingBoxes
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Int32

class ImageRecognition():
    def __init__(self):
        self.male_early_20s_bbox = BoundingBox()
        self.female_late_10s_bbox = BoundingBox()
        self.male_50s_bbox = BoundingBox()
        self.speechflag_male_early_20s = 0
        self.speechflag_female_late_10s = 0
        self.speechflag_male_50s = 0
        self.pub_speaker = rospy.Publisher("/tts", String, queue_size = 10)
        #self.pub_wp_navi_flag = rospy.Publisher("/wp_navi_flag", Int32, queue_size = 10)
        rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, self.recognitionCB)
        #rospy.Subscriber("/person_recog_flag", Int32, self.person_recog_flagCB)

    def recognitionCB(self, msg):
        bboxs = msg.bounding_boxes

        male_early_20s_bbox = BoundingBox()
        female_late_10s_bbox = BoundingBox()
        male_50s_bbox = BoundingBox()

        if len(bboxs) != 0:
            for i, bb in enumerate(bboxs):
                if bboxs[i].Class == "MaleEarly20s":
                    male_early_20s_bbox = bboxs[i]

                if bboxs[i].Class == "FemaleLate10s":
                    female_late_10s_bbox = bboxs[i]

                if bboxs[i].Class == "Male50s":
                    male_50s_bbox = bboxs[i]

        self.male_early_20s_bbox = male_early_20s_bbox
        self.female_late_10s_bbox = female_late_10s_bbox
        self.male_50s_bbox = male_50s_bbox

    # 本来Robocupではguestの年齢層を直前まで把握できないが
    # 今回は研究室内で行うため年齢層を便宜上 3クラスとした
    # 大会出場の際は考えられるすべての年齢層のデータセット等からクラス数を増やす必要がある
    def speech_flag_and_print(self):
        rate = rospy.Rate(2.0) 

        while not rospy.is_shutdown():
            print("male_early_20s: " + str(self.male_early_20s_bbox) + "\n")
            print("female_late_10s: " + str(self.female_late_10s_bbox) + "\n")
            print("male_50s: " + str(self.male_50s_bbox) + "\n")

            if self.male_early_20s_bbox.Class == "MaleEarly20s":
                print("About a Person, He is man.")
                print("His age is considered in his early twenties.")
                self.speechflag_male_early_20s = 1
                # break

            if (self.female_late_10s_bbox.Class == "FemaleLate10s"
                and self.female_late_10s_bbox.probability >= 98):
                print("About a Person, She is woman.")
                print("Her age is considered in her late teens.")
                self.speechflag_female_late_10s = 1
                # break

            if self.male_50s_bbox.Class == "Male50s":
                print("About a Person, He is old man.")
                print("His age is considered in his fifties.")
                self.speechflag_male_50s = 1
                # break

            if (self.speechflag_male_early_20s == 1
                or self.speechflag_female_late_10s == 1
                or self.speechflag_male_50s == 1):
                print("male_early_20s_Flag: " + str(self.speechflag_male_early_20s))
                print("female_late_10s_flag: " + str(self.speechflag_female_late_10s))
                print("male_50s_Flag: " + str(self.speechflag_male_50s))
                break
            rate.sleep()
 
    def speech_speak(self):
        self.words_container = ["About a Person",
                                "One Person's gender is male.",
                                "One Person's gender is female.",
                                "His age is considered in his early twenties. So, He is male student at KIT.",
                                "Her age is considered in her late teens. So, She is female student at KIT.",
                                "His age is considered in his fifties. So, He is teacher.",
                                "Next to her is the male student I mentioned earlier.",
                                "Next to him is student I mentioned earlier."]

        print("speech start.")

        if self.speechflag_male_early_20s == 1:
            self.pub_speaker.publish(self.words_container[0])
            time.sleep(2.0)
            self.pub_speaker.publish(self.words_container[1])
            time.sleep(3.0)
            self.pub_speaker.publish(self.words_container[3])
            time.sleep(3.5)

        if self.speechflag_female_late_10s == 1:
            self.pub_speaker.publish(self.words_container[0])
            time.sleep(2.0)
            self.pub_speaker.publish(self.words_container[2])
            time.sleep(3.0)
            self.pub_speaker.publish(self.words_container[4])
            time.sleep(3.5)
            if self.speechflag_male_early_20s == 1:
                self.pub_speaker.publish(self.words_container[6])
                time.sleep(3.0)

        if self.speechflag_male_50s == 1:
            self.pub_speaker.publish(self.words_container[0])
            time.sleep(2.0)
            self.pub_speaker.publish(self.words_container[1])
            time.sleep(3.0)
            self.pub_speaker.publish(self.words_container[5])
            time.sleep(3.0)
            if (self.speechflag_male_early_20s == 1
                or self.speechflag_female_late_10s == 1):
                self.pub_speaker.publish(self.words_container[7])
                time.sleep(3.5)

        self.speechflag_male_early_20s = 0
        self.speechflag_female_late_10s = 0
        self.speechflag_male_50s = 0
        print("speech finished.")

        """
        for i, words in enumerate(self.words_container):
            # 中身の条件をもう少し厳密指定する
            if self.speechflag_male_early_20s == 1:
                if i == 0 or i == 1 or i == 3:
                    self.pub_speaker.publish(words)
                    time.sleep(3.5)
                elif i == 5:
                    self.speechflag_male_early_20s = 0
                else:
                    continue

            elif self.speechflag_female_late_10s == 1:
                if i == 0 or i == 2 or i == 4:
                    self.pub_speaker.publish(words)
                    time.sleep(3.5)
                elif i == 5:
                    self.speechflag_female_late_10s = 0
                else:
                    continue

            elif self.speechflag_male_50s == 1:
                if i == 0 or i == 1:
                    self.pub_speaker.publish(words)
                    time.sleep(3.0)
                elif i == 5:
                    self.pub_speaker.publish(words)
                    time.sleep(3.0)
                    self.speechflag_male_50s = 0
                else:
                    continue
        """

if __name__ == "__main__":
    rospy.init_node("image_recog")
    img_recog = ImageRecognition()
    img_recog.speech_flag_and_print()
    img_recog.speech_speak()
