import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# CSV 파일 불러오기 (절대경로!)
df = pd.read_csv("/home/garam/ros_rs/rosbag_data/week05_ex2.csv")

# 시작점과 목표점
start_x, start_y = 2.0, 2.0
goal_x, goal_y = 4.0, 3.0

# 전체 목표 거리
total_distance = np.sqrt((goal_x - start_x)**2 + (goal_y - start_y)**2)

# 시간, 위치 데이터 가져오기
time = df["%time"].to_numpy()
x = df["field.pose.pose.position.x"].to_numpy()
y = df["field.pose.pose.position.y"].to_numpy()

# 시간 나노초 → 초로 변환
time_sec = (time - time[0]) / 1e9

# 현재 거리 오차 계산
distance_to_goal = np.sqrt((goal_x - x)**2 + (goal_y - y)**2)

# System response: 목표와 얼마나 가까워졌는가 (정규화)
response = 1 - (distance_to_goal / total_distance)
response = np.clip(response, 0, 1)  # 0~1 사이로 제한

# 원하는 이상적인 응답 (목표 도달 상태)
desired = np.ones_like(response)

# 그래프 그리기
plt.figure(figsize=(8, 4))
plt.plot(time_sec, response, label="Actual response", color="blue")
plt.plot(time_sec, desired, label="Desired response", color="red", linestyle='--')
plt.title("System Response - week05 ex2 graph")
plt.xlabel("Time (s)")
plt.ylabel("Response")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
