import numpy as np
import matplotlib.pyplot as plt

# 生成正常的时序数据
np.random.seed(42)
time_steps = 100
normal_data = np.random.normal(loc=0, scale=1, size=time_steps)

# 添加全局点异常
start_time = 30
end_time = 40
amplitude = 5
normal_data[start_time:end_time] += amplitude

# 画出图像，并用红色圆点标记异常点
plt.plot(normal_data)
plt.scatter(range(start_time, end_time), normal_data[start_time:end_time], color='red')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend()
plt.show()
