import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV 파일 불러오기
odom_df = pd.read_csv("/home/garam/ros_rs/rosbag_data/ex3_odom.csv")

# 시간 (초 단위로 정규화 후 numpy 배열로 변환)
odom_time = ((odom_df["%time"] - odom_df["%time"].iloc[0]) / 1e9).to_numpy()

# 위치 정보
x = odom_df["field.pose.pose.position.x"]
y = odom_df["field.pose.pose.position.y"]

# 쿼터니언 → yaw 계산
qz = odom_df["field.pose.pose.orientation.z"]
qw = odom_df["field.pose.pose.orientation.w"]
yaw = np.arctan2(2 * qw * qz, 1 - 2 * qz**2)

# 목표 위치
goal_x, goal_y = 1.5, 1.5
dx = goal_x - x
dy = goal_y - y
goal_yaw = np.arctan2(dy, dx)

# yaw 오차 [-pi, pi]로 정규화
error = goal_yaw - yaw
error = np.arctan2(np.sin(error), np.cos(error))

# 응답 곡선 계산: 목표에 가까울수록 1
response = 1 - np.abs(error) / np.pi
response = np.clip(response, 0, 1).to_numpy()

# 이상적 응답 (항상 1)
desired = np.ones_like(response)

# 그래프 출력
plt.figure(figsize=(10, 4))
plt.plot(odom_time, response, label="Yaw Response", color="blue")
plt.plot(odom_time, desired, label="Desired", color="red", linestyle="--")
plt.xlabel("Time (s)")
plt.ylabel("Normalized Angular Response")
plt.title("System Response (PID Yaw Control)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
