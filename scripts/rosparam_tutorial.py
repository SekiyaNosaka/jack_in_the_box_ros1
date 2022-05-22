#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ROS
import rospy

class ParamTest:
    def __init__(self):
        self.param_1 = rospy.get_param("/tokyo")
        self.param_2 = rospy.get_param("/osaka")
        self.param_3 = rospy.get_param("/nagoya")
        self.param_4 = rospy.get_param("/member")
        self.param_5 = rospy.get_param("/member/name")
        self.param_6 = rospy.get_param("/member/id")
        self.param_7 = rospy.get_param("/member_list")
        self.param_8 = rospy.get_param("/nums_list")
        self.param_9 = rospy.get_param("/Country_A")

    def param_print(self):
        print(self.param_1)
        print(self.param_2)
        print(self.param_3)
        print(self.param_4)
        print(self.param_5)
        print(self.param_6)
        print(self.param_7)
        print(self.param_8)
        print(self.param_9)
        
        # result -> all managed by "str"
        print(type(self.param_1),
              type(self.param_2),
              type(self.param_3),
              type(self.param_4),
              type(self.param_5),
              type(self.param_7),
              type(self.param_8),
              type(self.param_9))

if __name__ == "__main__":
    rospy.init_node("rosprm_tutorial")
    pt = ParamTest()
    pt.param_print()
    rospy.spin()
