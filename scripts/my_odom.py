#!/usr/bin/env python

# General
import time
import math

# ROS
import rospy
import tf
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist, Vector3
from nav_msgs.msg import Odometry

class Kobuki():
    def __init__(self):
        self.pos_fhi = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.r = 0.038  # kobuki's wheel_radius
        self.d = 0.12   # kobuki's wheel_distance
        self.wheel_right_jointstate_pos_init = 0.0
        self.wheel_left_jointstate_pos_init  = 0.0
        self.start = time.time()
        rospy.Subscriber("/joint_states", JointState, self.deadreckoning)

    def deadreckoning(self, jointstate):
        if time.time() - self.start >= 0.05:
            self.start = time.time()

            self.wheel_right_jointstate_pos = jointstate.position[0]
            self.wheel_left_jointstate_pos  = jointstate.position[1]

            self.wheel_right_jointstate_vel = (self.wheel_right_jointstate_pos - self.wheel_right_jointstate_pos_init) / 0.05
            self.wheel_left_jointstate_vel  = (self.wheel_left_jointstate_pos  - self.wheel_left_jointstate_pos_init)  / 0.05

            self.wheel_right_jointstate_pos_init = self.wheel_right_jointstate_pos
            self.wheel_left_jointstate_pos_init  = self.wheel_left_jointstate_pos
            self.pos_fhi += (((0.5 * self.r) / self.d) * (self.wheel_right_jointstate_vel - self.wheel_left_jointstate_vel)) * 0.05
            self.pos_x   += (0.5 * self.r * (self.wheel_right_jointstate_vel + self.wheel_left_jointstate_vel) * math.sin(self.pos_fhi)) * 0.05
            self.pos_y   += (0.5 * self.r * (self.wheel_right_jointstate_vel + self.wheel_left_jointstate_vel) * math.cos(self.pos_fhi)) * 0.05
            rospy.loginfo(self.pos_fhi, self.pos_x, self.pos_y)

if __name__ == "__main__":
    try:
        rospy.init_node("odom_deadreconing", anonymous = True)
        Kobuki()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
