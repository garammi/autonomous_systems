#!/usr/bin/env python3
import rospy
from std_srvs.srv import SetBool,SetBoolResponse
from std_msgs.msg import Int32

temp = 25

def handle_service_request(req):
    rospy.loginfo("서비스 요청 받음: %s",req.data)
    rospy.loginfo("현재 온도: %d",temp)
    
    if temp >= 30:
        msg = "turn on"
    else:
        msg = "turn off"
        
    rospy.loginfo(msg)
    response = SetBoolResponse()
    response.success = True
    response.message = "서비스 요청이 성공적으로 처리되었습니다."
    return response

def temp_sub(msg):
    global temp 
    temp = msg.data
    

def simple_service_server():
    rospy.init_node("simple_service_server")
    rospy.Subscriber("temperature",Int32,temp_sub)
    service = rospy.Service("set_fan_state",SetBool,handle_service_request)
    rospy.loginfo("서비스 서버 시작: /set_fan_state")
    rospy.spin()

if __name__ == "__main__":
    simple_service_server()
