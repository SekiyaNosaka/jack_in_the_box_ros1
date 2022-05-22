#!/usr/bin/env python
# -*- coding: utf-8 -*-

# General
import time
import math

# ROS
import rospy
import tf
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Quaternion

class Robot:
    def __init__(self):
        self.pub_1 = rospy.Publisher("/cmd_vel_mux/input/teleop",
                                     Twist, queue_size = 10)
        self.pub_2 = rospy.Publisher("/tts", String, queue_size = 10)
        rospy.Subscriber("/odom", Odometry, self.odomCallBack)
        self.vel = Twist() 
        self.vel.linear.x = self.vel.linear.y = self.vel.linear.z = 0.0
        self.vel.angular.x = self.vel.angular.y = self.vel.angular.z = 0.0
        self.Pose = [0.0, 0.0, 0.0]
        self.pos_x = self.pos_y = 0.0

    def speech(self):
        self.words = ["Hello.",
                      "My name is Taro.",
                      "I'm hungry."]
        for i in range(3):
            self.pub_2.publish("There are 3 Person.")
            time.sleep(4)
            self.pub_2.publish("Male are 2 Person.")
            time.sleep(4)
            self.pub_2.publish("Female are 1 Person.")
            time.sleep(4)

    def setLinearVel(self, linear_vel):
        self.vel.linear.x = linear_vel
        self.pub.publish(self.vel)
    
    def setAngularVel(self, angular_vel):
        self.vel.angular.z = angular_vel
        self.pub.publish(self.vel)

    def setVel(self, linear_vel, angular_vel = 0):
        self.vel.linear.x = linear_vel
        self.vel.angular.z = angular_vel
        self.pub.publish(self.vel)

    def odomCallBack(self, msg):
        self.pos_x = msg.pose.pose.position.x
        self.pos_y = msg.pose.pose.position.y
        self.q = tf.transformations.euler_from_quaternion((msg.pose.pose.orientation.x,
                                                           msg.pose.pose.orientation.y,
                                                           msg.pose.pose.orientation.z,
                                                           msg.pose.pose.orientation.w))
        self.Pose[:3] = self.pos_x, self.pos_y, self.q[2]

    def moveToDistance(self, linear_vel, dist):
        self.d = 0.0
        self.init_pos_x, self.init_pos_y = self.Pose[:2]
        while self.d <= dist:
            self.setVel(linear_vel)
            self.d = math.sqrt((self.pos_x - self.init_pos_x)**2 + (self.pos_y - self.init_pos_y)**2)
            print(self.d)
        self.setVel(0.0)

    def turnToAngle(self, ang_vel, angle):
        self.a = 0.0
        self.init_pos_theta = self.Pose[2]
        while abs(self.a) <= abs(angle):
            self.setVel(0.0, ang_vel)
            self.a = self.Pose[2] - self.init_pos_theta
            print(self.a)
            print(self.Pose[2])
        self.setVel(0.0)

if __name__ == "__main__":
    try:
        rospy.init_node("my_robot")
        r = Robot()
        r.speech()
        # deadreckoning = my_odom.HappyMini()
        # r.turnToAngle(0.3, 2.0)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
