#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time

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

    rospy.init_node('ex3_pid_controller')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/odom', Odometry, odom_cb)
    rate = rospy.Rate(10)

    cmd = Twist()

    # PID gains for angle
    Kp_ang = 6.0
    Ki_ang = 1.0
    Kd_ang = 2.0

    # PID gains for distance
    Kp_lin = 1.0
    Ki_lin = 0.0
    Kd_lin = 0.2

    # angle
    Kp_ang = 4.0
    Ki_ang = 0.2
    Kd_ang = 3.0

    # distance
    Kp_lin = 0.9
    Ki_lin = 0.03
    Kd_lin = 0.25


    int_ang = 0.0
    prev_ang = 0.0

    int_dist = 0.0
    prev_dist = 0.0

    prev_time = time.time()

    while not rospy.is_shutdown() and (x is None or y is None or yaw is None):
        rate.sleep()

    while not rospy.is_shutdown():
        dx = x_goal - x
        dy = y_goal - y
        dist = math.sqrt(dx**2 + dy**2)
        goal_ang = math.atan2(dy, dx)
        ang_err = goal_ang - yaw
        ang_err = math.atan2(math.sin(ang_err), math.cos(ang_err))

        # 시간 계산
        current_time = time.time()
        dt = current_time - prev_time if current_time != prev_time else 1e-6

        # PID for angle
        int_ang += ang_err * dt
        der_ang = (ang_err - prev_ang) / dt
        wz = Kp_ang * ang_err + Ki_ang * int_ang + Kd_ang * der_ang

        # PID for distance (linear speed)
        int_dist += dist * dt
        der_dist = (dist - prev_dist) / dt
        vx = Kp_lin * dist + Ki_lin * int_dist + Kd_lin * der_dist
        vx = max(0.0, min(vx, 0.3))  # 속도 제한

        rospy.loginfo(f"[x={x:.2f}, y={y:.2f}] dist={dist:.2f}, ang_err={ang_err:.2f}, vx={vx:.2f}, wz={wz:.2f}")

        if dist < 0.01:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            pub.publish(cmd)
            rospy.loginfo("finish")
            break
        else:
            cmd.linear.x = vx
            cmd.angular.z = wz

        pub.publish(cmd)

        prev_ang = ang_err
        prev_dist = dist
        prev_time = current_time
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
