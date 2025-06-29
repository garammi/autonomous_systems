#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

current_x = 0.0
start_x = None

def odom_callback(msg):
    global current_x, start_x
    current_x = msg.pose.pose.position.x
    if start_x is None:
        start_x = current_x
        rospy.loginfo("start")

def move():
    global current_x, start_x

    rospy.init_node('move_to_dest')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, odom_callback)

    rate = rospy.Rate(10)
    cmd = Twist()

    while not rospy.is_shutdown():
        if start_x is None:
            rate.sleep()
            continue

        distance = abs(current_x - start_x)

        if distance < 1.0:  
            cmd.linear.x = 0.2
            cmd.angular.z = 0.0
        else:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            rospy.loginfo("stop")

        pub.publish(cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass
