#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32
import random

def temp_publisher():
    rospy.init_node('temp_publisher',anonymous=True)
    pub = rospy.Publisher('temperature',Int32,queue_size=10)
    rate = rospy.Rate(0.2)
    
    while not rospy.is_shutdown():
        temp= random.randint(10,40)
        rospy.loginfo("Tempurature : %d",temp)
        pub.publish(temp) 
        rate.sleep()
        
if __name__ == '__main__':
    try:
        temp_publisher()
    except rospy.ROSInterruptException:
        pass
