#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ROS
import rospy
from jack_in_the_box.srv import MySrv

class MyClient():
    def call_service(self):
        rospy.init_node("self_service_client")
        rospy.wait_for_service("self_call_me")
        try:
            while(True):
                service = rospy.ServiceProxy("self_call_me", MySrv)
                resp = service("a", "b")
                rospy.loginfo(resp)
                rospy.sleep(1.0)
        except rospy.ServiceException as e:
            rospy.warn(e)

if __name__ == "__main__":
    mc = MyClient()
    mc.call_service()
