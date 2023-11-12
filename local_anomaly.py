import numpy as np
import matplotlib.pyplot as plt

# 生成正常的时序数据
np.random.seed(42)
time_steps = 100
normal_data = np.random.normal(loc=0, scale=1, size=time_steps)

# 添加随机局部点异常
num_anomalies = 5
anomaly_indices = np.random.choice(time_steps, num_anomalies, replace=False)
amplitude = 3

for idx in anomaly_indices:
    normal_data[idx] += amplitude

# 画出图像，并用红色圆点标记异常点
plt.plot(normal_data)
plt.scatter(anomaly_indices, normal_data[anomaly_indices], color='red')
# plt.title('Time Series Data with Random Local Anomalies')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()
