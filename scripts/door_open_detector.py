#!/usr/bin/env python

# General
import time

# ROS
import rospy
import my_robot
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

LASER_SCAN_RESOLUTION = 1080 # Hokuyo Lidar's resolution

class DoorOpenDetector:
    def __init__(self):
        self.action_for_my_robot = my_robot.Robot()
        self.get_laser_value = 999
        self.r = rospy.Rate(10)
        rospy.wait_for_message("/scan", LaserScan)
        rospy.Subscriber("/scan", LaserScan, self.getLaserScanValue)

    def getLaserScanValue(self, msg):
        self.get_laser_value = msg.ranges[LASER_SCAN_RESOLUTION/2]

    def avoidObstacle(self):
      while not rospy.is_shutdown():
            if self.get_laser_value <= 1.0:
                while not self.get_laser_value >= 4.0:
                    self.r.sleep()
                self.action_for_my_robot.setVel(0.3, 2.0)
                break
            else:
                self.action_for_my_robot.setVel(0.1)

if __name__ == "__main__":
    rospy.init_node("door_open_detect")
    d = DoorOpenDetector()
    d.avoidObstacle()
