#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ROS
import rospy
from jack_in_the_box.srv import MySrv, MySrvResponse

class MyServer():
    def handle_service(self, req):
        rospy.loginfo("called")
        rospy.loginfo(req.info1)
        rospy.loginfo(req.info2)
        return MySrvResponse(True)

    def service_server(self):
        rospy.init_node("self_service_server")
        rospy.Service("self_call_me", MySrv, self.handle_service)
        rospy.loginfo("Ready to serve")
        rospy.spin()

if __name__ == "__main__":
    ms = MyServer()
    ms.service_server()
