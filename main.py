# This is a sample Python script.
from scipy.spatial.transform import Rotation as R
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
from matplotlib import pyplot
import numpy
import random


# xy in a frame 1 to a frame 2 whose origin lies at dx,dy in frame 1 and rotated by rot
def convert(x, y, dx, dy, rot):
    cos_rot = math.cos(math.radians(rot))
    sin_rot = math.sin(math.radians(rot))
    x_translated = x - dx
    y_translated = y - dy
    x_rotated = cos_rot * x_translated + sin_rot * y_translated
    y_rotated = -sin_rot * x_translated + cos_rot * y_translated
    return x_rotated, y_rotated

def plot_history(history, color):
    n = history.shape[0]
    ones = numpy.ones(n) * 0.01
    pyplot.plot(history[:, 0], history[:, 1], color, alpha=0.5)
    pyplot.quiver(history[:, 0], history[:, 1], ones, ones, angles=history[:, 2], zorder=100)


class Frames:
    def __init__(self):
        self.position = numpy.array([0.0, 0.0])
        self.orientation = 0.0
        self.eye_orientation = 0.0
        self.crab_trace = []
        self.crab_trace.append(self.state)

    def walk(self, rotation=0, distance=0):
        self.orientation = self.orientation + rotation
        radians = math.radians(self.orientation)
        dx = math.sin(radians) * distance
        dy = math.cos(radians) * distance
        self.position[0] = self.position[0] + dx
        self.position[1] = self.position[1] + dy

        self.crab_trace.append(self.state)

    def crab2world(self, x, y, eye=False):
        dx = self.state[0]
        dy = self.state[1]
        rot = self.state[2]
        if eye: rot = rot + self.state[3]
        x, y = convert(x, y, -dx, -dy, -rot)
        return x, y

    def world2crab(self, x, y, eye=False):
        dx = self.state[0]
        dy = self.state[1]
        rot = self.state[2]
        if eye: rot = rot + self.state[3]
        x, y = convert(x, y, dx, dy, rot)
        return x, y

    def saccade(self, rotation=0):
        self.eye_orientation = self.eye_orientation + rotation

    def print_state(self):
        crab_message = 'X=%.4f, Y=%.4f, ROT=%.4f, EYE=%.4f' % self.state
        print(crab_message)

    @property
    def state(self):
        x = self.position[0]
        y = self.position[1]
        rot = self.orientation
        eye = self.eye_orientation
        return x, y, rot, eye

    @property
    def history(self):
        array = numpy.array(self.crab_trace)
        return array


class Crab:
    def __init__(self):
        self.estimated_frames = Frames()
        self.real_frames = Frames()

    def walk(self, rotation, translation, update_estimation=True):
        self.real_frames.walk(rotation, translation)
        if update_estimation: self.estimated_frames.walk(rotation, translation)

    def saccade(self, rotation, update_estimation=True):
        self.real_frames.saccade(rotation)
        if update_estimation: self.estimated_frames.saccade(rotation)

    def print_states(self):
        print('Real state:')
        self.real_frames.print_state()
        print('Estimated state:')
        self.estimated_frames.print_state()

    def estimated_burrow_location(self):
        estimated_x = self.estimated_frames.state[0]
        estimated_y = self.estimated_frames.state[1]
        x, y = self.real_frames.crab2world(-estimated_x, -estimated_y)
        print('estimated', x, y)
        return x, y

    def plot(self):
        real_history = self.real_frames.history
        estimated_history = self.estimated_frames.history
        plot_history(real_history, color='r-')
        plot_history(estimated_history, color='g--')
        x, y = self.estimated_burrow_location()
        pyplot.scatter(x, y, color='g', s=100)
        pyplot.scatter(0, 0, color='r', s=100)
        pyplot.grid()
        ax = pyplot.gca()
        ax.set_aspect('equal', 'box')
        pyplot.show()


c = Crab()

for i in range(5):
    distance = random.random() * 100
    rotation = random.random() * 180 - 90
    update = True
    if i > 3:
        update = False
        rotation = 0
    c.walk(rotation, distance, update_estimation=update)

c.print_states()
c.plot()
print(c.real_frames.world2crab(0,0))