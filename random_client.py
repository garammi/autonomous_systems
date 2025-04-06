#!/usr/bin/env python3

import rospy
import actionlib
from my_custom_pkg.msg import RandomNAction, RandomNGoal

def feedback_cb(feedback):
    rospy.loginfo(f"현재 숫자 list: {feedback.current_list}")

def main():
    rospy.init_node('random_client')

    client = actionlib.SimpleActionClient('random_number', RandomNAction)
    client.wait_for_server()


    goal_count = rospy.get_param('/goal_number', 5)

    goal = RandomNGoal()
    goal.goal_count = goal_count

    client.send_goal(goal, feedback_cb=feedback_cb)
    rospy.loginfo(f"요청한 숫자 개수: {goal_count}")

    client.wait_for_result()
    result = client.get_result()

    rospy.loginfo(f"최종 숫자 list: {result.result_list}")

if __name__ == '__main__':
    main()

