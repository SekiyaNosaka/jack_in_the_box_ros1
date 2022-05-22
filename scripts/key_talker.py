#!/usr/bin/env python

# ROS
import rospy
import tf
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def main():
    rospy.init_node("talker")
    pub = rospy.Publisher("/cmd_vel_mux/input/teleop",
                          Twist,
                          queue_size = 10)
    
    r = rospy.Rate(10)
    vel = Twist()
    while not rospy.is_shutdown():
        key = input()
        print(key, "is input")
        if key == 1: vel.linear.x = 0.4
        elif key == 2: vel.linear.x = -0.4
        elif key == 3: vel.angular.z = 0.3
        elif key == 4: vel.angular.z = -0.3
        else: break
        pub.publish(vel)
        vel.linear.x = 0.0
        vel.angular.z = 0.0
        r.sleep()

if __name__ == "__main__":
    main()
