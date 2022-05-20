import random

import cv2
import gym # i used 0.10.5
from matplotlib import pyplot as plt

env = gym.make('Pong-v4')
observation = env.reset()
plt.imshow(observation)
for i in range(30):
#     observation, reward, done, info = env.step(0)  # 0 means stay the same place(or do nothing)
#     plt.imshow(observation)
#     plt.show()
    print(type(random.choice([1, -1])))