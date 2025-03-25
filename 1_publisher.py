#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import random
from datetime import datetime

def publisher():
    rospy.init_node('seohi', anonymous=True)  # ← 이름 수정
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rate = rospy.Rate(0.2)  # ← 5초마다 1회 (1 / 5초 = 0.2Hz)

    while not rospy.is_shutdown():
        num = random.randint(1, 100)
        now = datetime.now().strftime('%H:%M:%S')
        msg = f"[{now}] Random Number: {num}"
        rospy.loginfo("Publishing: %s", msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
