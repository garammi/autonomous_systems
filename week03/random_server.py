#!/usr/bin/env python3

import rospy
import time
import random
import actionlib
from my_custom_pkg.msg import RandomNAction, RandomNResult, RandomNFeedback

def execute_cb(goal):
    count = goal.goal_count  # 뽑을 숫자 개수
    feedback = RandomNFeedback()
    result = RandomNResult()

    nums = set()  # 뽑은 숫자 저장 list

    while len(nums) < count and not server.is_preempt_requested():
        n = random.randint(15, 30) 

        if n not in nums:  #중복확인
            nums.add(n)  
            feedback.current_list = list(nums)  
            server.publish_feedback(feedback)
            rospy.loginfo(f"생성된 숫자: {n}")
            time.sleep(1)  

    result.result_list = list(nums)
    server.set_succeeded(result)
    rospy.loginfo("finish")

def main():
    global server
    rospy.init_node('random_server')

    server = actionlib.SimpleActionServer(
        'random_number', RandomNAction, execute_cb, False
    )

    server.start()
    rospy.loginfo("Random Number Action Server Started")
    rospy.spin()

if __name__ == '__main__':
    main()

