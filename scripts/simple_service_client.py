#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ROS
import rospy
from std_srvs.srv import Trigger

class Client():
    def call_service(self):
        rospy.init_node("simple_service_client")
        rospy.wait_for_service("simple_call_me")
        service = rospy.ServiceProxy("simple_call_me", Trigger)
        try:
            resp = service()
            rospy.loginfo(resp.success)
            rospy.loginfo(resp.message)
        except rospy.ServiceException as e:
            rospy.warn(e)

if __name__ == "__main__":
    cl = Client()
    cl.call_service()
