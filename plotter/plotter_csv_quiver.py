import math
import time

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.canvas.mpl_connect('close_event', lambda evt: quit())

with open('data/magnet.csv', 'r') as f:
    dots = f.readlines()

x0, y0, z0 = -13.63, 17.25, -75.88

xs, ys, zs, cs = [], [], [], []
t = 0

for dot in dots:
    xyz = dot.split()
    x, y, z = float(xyz[0]) - x0, float(xyz[1]) - y0, float(xyz[2]) - z0 + t
    xs.append(x), ys.append(y), zs.append(z)

    # vector length is color!
    cs.append(math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))

    # ax.cla()
    ax.quiver(0, 0, t, x, y, z - t)
    ax.plot([x], [y], [z])

    plt.draw()
    plt.pause(0.001)
    t += 1

ax.scatter(xs, ys, zs, c=cs, cmap='cool', s=1)

while True:
    plt.draw()
    plt.pause(0.001)
