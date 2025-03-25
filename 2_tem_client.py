#!/usr/bin/env python3
import rospy
from std_srvs.srv import SetBool


def simple_service_client():
    rospy.init_node("simple_service_client")
    rospy.wait_for_service("set_fan_state")
    try: 
        service_proxy = rospy.ServiceProxy("set_fan_state",SetBool)
        response = service_proxy(True)
        rospy.loginfo("응답 받음 : %s",response.message)
    except rospy.ServiceException as e:
        rospy.logerr("서비스 요청 실패: %s",e)


if __name__ == "__main__":
    simple_service_client()