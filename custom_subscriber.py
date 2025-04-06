#!/usr/bin/env python3

import rospy
from my_custom_pkg.msg import Motion  # 커스텀 메시지 임포트

position=[0,0]

def motion_callback(data):    
    position[0] = data.move_x
    position[1] = data.move_y
    rospy.loginfo(f"Position: ({position[0]}, {position[1]})")

def motion_subscriber():
    rospy.init_node('motion_subscriber', anonymous=True)
    rospy.Subscriber('motion_info', Motion, motion_callback)
    rospy.spin()  # 콜백 함수가 계속 실행될 수 있도록 유지

if __name__ == '__main__':
    motion_subscriber()


