import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("/home/garam/ros_rs/rosbag_data/week05_ex1.csv")


time = df["%time"].to_numpy()
x_pos = df["field.pose.pose.position.x"].to_numpy()
time = (time - time[0]) / 1e9  

x_goal = 1.5

plt.figure(figsize=(8, 5))
plt.plot(time, x_pos, label="Actual response", color='blue', linewidth=2)
#plt.axhline(y=x_goal, color='red', linestyle='--', label="Desired response (x=1.5)")
plt.xlabel("Time (s)")
plt.ylabel("X Position (m)")
plt.title("week05 - ex1 graph")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
