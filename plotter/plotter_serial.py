import math
import time

import matplotlib.pyplot as plt
import serial

# init serial - source for the data
SERIAL_PORT = '/dev/tty.usbmodem14201'  # path to serial output
SERIAL_RATE = 9600
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)

# data to be displayed on plot
last_x, last_y, last_z = None, None, None
xs, ys, zs, cs = [], [], [], []
new_points_count = 0

# init plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
fig.canvas.mpl_connect('close_event', lambda evt: quit())

while True:

    try:
        xyz = ser.readline().decode('utf-8').split()
        if last_x is None:
            last_x = float(xyz[0])
            last_y = float(xyz[1])
            last_z = float(xyz[2])

        x = float(xyz[0])
        y = float(xyz[1])
        z = float(xyz[2])

    # reconnect to serial on errors
    except serial.SerialException as se:
        print('Serial has errors, trying to reconnect. err:', se)
        time.sleep(3)
        ser.close()
        ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
        print('Serial reconnected!')

    except Exception as e:
        print("Bad read from serial:", xyz, e)
        continue

    # distance between current and last point in 3d
    distance_to_previous = math.sqrt(math.pow(x - last_x, 2) + math.pow(y - last_y, 2) + math.pow(z - last_z, 2))

    # if last point was too close, don't plot it
    if distance_to_previous > 0.75:
        xs.append(x)
        ys.append(y)
        zs.append(z)
        cs.append(math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))  # vector length
        last_x, last_y, last_z = x, y, z
        new_points_count += 1

    # remove old dots, smaller buffer gives higher refresh rate on plot
    if len(xs) > 256:
        xs.pop(0)
        ys.pop(0)
        zs.pop(0)
        cs.pop(0)

    if new_points_count > 1:
        ax.cla()
        ax.scatter(xs, ys, zs, c=cs, cmap='cool')
        new_points_count = 0

    plt.draw()
    plt.pause(0.001)
