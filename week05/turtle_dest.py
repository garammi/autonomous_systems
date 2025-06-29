#!/usr/bin/env python3
import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

x = 0.0
y = 0.0
yaw = 0.0

goal_x = 2.0
goal_y = 1.0

def callback(msg):
    global x, y, yaw

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    
    q = msg.pose.pose.orientation
    sin = 2 * (q.w * q.z + q.x * q.y)
    cos = 1 - 2 * (q.y * q.y + q.z * q.z)
    yaw = math.atan2(sin, cos)

def simple_p_controller():
    rospy.init_node('simple_p_goal')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, callback)

    move = Twist()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        
        dx = goal_x - x
        dy = goal_y - y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist > 0.1:
            target_angle = math.atan2(dy, dx)
            error = target_angle - yaw
            move.linear.x = 0.2
            move.angular.z = 1.5 * error  
        else:
            move.linear.x = 0.0
            move.angular.z = 0.0
            rospy.loginfo("finish")

        pub.publish(move)
        rate.sleep()

if __name__ == '__main__':
    try:
        simple_p_controller()
    except rospy.ROSInterruptException:
        pass



'''#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math

x, y, yaw = None, None, None  
x_goal = 1.5
y_goal = 1.5

def odom_cb(msg):
    global x, y, yaw

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    q = msg.pose.pose.orientation
    siny = 2.0 * (q.w * q.z + q.x * q.y)
    cosy = 1.0 - 2.0 * (q.y**2 + q.z**2)
    yaw = math.atan2(siny, cosy)

def main():
    global x, y, yaw

    rospy.init_node('ex2_p_controller')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, odom_cb)
    rate = rospy.Rate(10)

    cmd = Twist()
    Kp = 3.0

    
    while not rospy.is_shutdown() and (x is None or y is None or yaw is None):
        rate.sleep()

    

    while not rospy.is_shutdown():
        dx = x_goal - x
        dy = y_goal - y
        dist = math.sqrt(dx**2 + dy**2)
        goal_ang = math.atan2(dy, dx)
        err = goal_ang - yaw
        err = math.atan2(math.sin(err), math.cos(err))

        rospy.loginfo(f"[x={x:.2f}, y={y:.2f}] → 거리: {dist:.2f}, 각도오차: {err:.2f}")

        if dist < 0.01:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            pub.publish(cmd)
            break
        else:
            cmd.linear.x = 0.2
            cmd.angular.z = Kp * err

        pub.publish(cmd)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
'''
