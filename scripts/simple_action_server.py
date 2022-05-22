#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
from jack_in_the_box.msg import *

class MyServer():
    def __init__(self):
        self.ac_server = actionlib.SimpleActionServer('add_two_ints',
                                                    AddTwoIntsAction,
                                                    self.listener_callback,
                                                    False)
        self.ac_server.start()

    def listener_callback(self, goal):
        r = rospy.Rate(5)
        for i in range(10):
            feedback = AddTwoIntsFeedback(i * 0.1)
            self.ac_server.publish_feedback(feedback)
            r.sleep()

        result = AddTwoIntsResult(goal.a + goal.b)
        self.ac_server.set_succeeded(result)

def main():
    rospy.init_node("add_two_ints_server")
    server = MyServer()
    rospy.spin()

if __name__ == "__main__":
    main()
