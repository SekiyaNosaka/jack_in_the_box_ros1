#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ROS
import rospy
from std_srvs.srv import Trigger, TriggerResponse

class Server():
    def handle_service(self, req):
        rospy.loginfo("called")
        return TriggerResponse(True, "success!")

    def service_server(self):
        rospy.init_node("simple_service_server")
        rospy.Service("simple_call_me", Trigger, self.handle_service)
        rospy.loginfo("Ready to serve")
        rospy.spin()

if __name__ == "__main__":
    sv = Server()
    sv.service_server()
