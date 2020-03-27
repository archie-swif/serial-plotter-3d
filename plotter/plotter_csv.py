import math
import time

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.canvas.mpl_connect('close_event', lambda evt: quit())

with open('data/magnet.csv', 'r') as f:
    dots = f.readlines()

xs, ys, zs, cs = [], [], [], []

for dot in dots:
    xyz = dot.split()
    x, y, z = float(xyz[0]), float(xyz[1]), float(xyz[2])
    xs.append(x), ys.append(y), zs.append(z)

    # vector length is color!
    cs.append(math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))

    ax.cla()
    ax.scatter(xs, ys, zs, c=cs, cmap='cool')
    plt.draw()
    plt.pause(0.001)

while True:
    plt.draw()
    plt.pause(0.001)
