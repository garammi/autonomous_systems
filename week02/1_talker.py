#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import random
from datetime import datetime

def publisher():
    rospy.init_node('garam', anonymous=True)  
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rate = rospy.Rate(0.2) 

    while not rospy.is_shutdown():
        num = random.randint(1, 100)
        now = datetime.now()
        msg = f"[{now}] random number: {num}"
        rospy.loginfo("Publishing: %s", msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
