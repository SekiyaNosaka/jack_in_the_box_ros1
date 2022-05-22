#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
from jack_in_the_box.msg import *

def feedback_callback(feedback):
    print("feedback :%f" %feedback.rate)

def main():
    rospy.init_node("add_two_ints_client")

    ac_client = actionlib.SimpleActionClient("add_two_ints", AddTwoIntsAction)

    ac_client.wait_for_server()

    a = 10
    b = 100
    goal = AddTwoIntsGoal(a, b)

    ac_client.send_goal(goal, feedback_cb = feedback_callback)

    ac_client.wait_for_result()
    result = ac_client.get_result()
    print("%s + %s = %s"%(a, b, result.sum))

if __name__ == "__main__":
   main()
