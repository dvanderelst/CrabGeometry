# This is a sample Python script.
from scipy.spatial.transform import Rotation as R
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
from matplotlib import pyplot
import numpy
import random


def plot_history(history, color):
    n = history.shape[0]
    ones = numpy.ones(n) * 0.01
    pyplot.plot(history[:, 0], history[:, 1], color, alpha=0.5)
    pyplot.quiver(history[:, 0], history[:, 1], ones, ones, angles=history[:, 2], zorder=100,color='r')
    pyplot.quiver(history[:, 0], history[:, 1], ones, ones, angles=history[:, 2]+90, zorder=100,color='g')


# xy in a frame 1 to a frame 2 whose origin lies at dx,dy in frame 1 and rotated by rot
def convert_tr(x, y, dx, dy, rot):
    cos_rot = math.cos(math.radians(rot))
    sin_rot = math.sin(math.radians(rot))
    x_translated = x - dx
    y_translated = y - dy
    x_rotated = cos_rot * x_translated + sin_rot * y_translated
    y_rotated = -sin_rot * x_translated + cos_rot * y_translated
    return x_rotated, y_rotated


# # xy in a frame 1 to a frame 2 whose origin lies at dx,dy in frame 1 and rotated by rot
def convert_rt(x, y, dx, dy, rot):
    cos_rot = math.cos(math.radians(rot))
    sin_rot = math.sin(math.radians(rot))

    x_rotated = cos_rot * x + sin_rot * y
    y_rotated = -sin_rot * x + cos_rot * y
    x_translated = x_rotated - dx
    y_translated = y_rotated - dy

    return x_translated, y_translated


class Frame:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0
        self.eye = 0.0
        self.trace = []
        self.trace.append(self.state)

    def step(self, rotation, distance):
        self.orientation = self.orientation + rotation
        radians = math.radians(self.orientation)
        dx = math.cos(radians) * distance
        dy = math.sin(radians) * distance
        self.x = self.x + dx
        self.y = self.y + dy
        self.trace.append(self.state)

    def print(self):
        print(self.x, self.y)

    def frame2world(self, x, y, eye=False):
        dx = self.x
        dy = self.y
        rot = self.orientation
        if eye: rot = rot + self.eye
        x, y = convert_rt(x, y, -dx, -dy, -rot)
        return x, y

    def world2frame(self, x, y, eye=False):
        dx = self.x
        dy = self.y
        rot = self.orientation
        if eye: rot = rot + self.eye
        x, y = convert_tr(x, y, dx, dy, rot)
        return x, y

    def move_eye(self, rotation=0):
        self.eye = self.eye + rotation

    def print_state(self):
        crab_message = 'X=%.4f, Y=%.4f, ROT=%.4f, EYE=%.4f' % self.state
        print(crab_message)

    @property
    def state(self):
        return self.x, self.y, self.orientation, self.eye

    @property
    def history(self):
        array = numpy.array(self.trace)
        return array


# f = Frame()
# f.step(0,100)
# f.step(-45,100)
# f.step(-1000,100)
# f.step(100000,1000)
# f.print_state()
#
# x = 99
# y = 123
#
# print('-----------------')
# print(x, y)
# x, y = f.frame2world(x,y)
# print(x, y)
# x,y = f.world2frame(x,y)
# print(x, y)
#
class Crab:
    def __init__(self):
        self.estimated_frame = Frame()
        self.real_frame = Frame()

    def step(self, rotation, translation, update_estimation=True):
        self.real_frame.step(rotation, translation)
        if update_estimation: self.estimated_frame.step(rotation, translation)

    def move_eye(self, rotation, update_estimation=True):
        self.real_frame.move_eye(rotation)
        if update_estimation: self.estimated_frame.move_eye(rotation)

    def estimated_burrow_location(self):
        dx = self.estimated_frame.x
        dy = self.estimated_frame.y
        x = self.real_frame.x - dx
        y = self.real_frame.y - dy
        return x, y

    def relative_estimated_burrow_location(self):
        x, y = self.estimated_burrow_location()
        x, y = self.estimated_frame.world2frame(x, y)
        return x, y

    def print_states(self):
        print('Real state:')
        self.real_frame.print_state()
        print('Estimated state:')
        self.estimated_frame.print_state()
        print('Estimated burrow:')
        x, y = self.estimated_burrow_location()
        print(x, y)
        print('Estimated burrow (relative):')
        x, y = self.relative_estimated_burrow_location()
        print(x, y)

    def plot(self):
        real_history = self.real_frame.history
        estimated_history = self.estimated_frame.history
        plot_history(real_history, color='k-')
        plot_history(estimated_history, color='b--')
        x, y = self.estimated_burrow_location()
        pyplot.scatter(x, y, color='b', s=100, alpha=0.5)
        pyplot.scatter(0, 0, color='k', s=100, alpha=0.5)
        pyplot.grid()
        ax = pyplot.gca()
        ax.set_aspect('equal', 'box')
        pyplot.show()


f = Crab()
f.step(0, 130)
f.step(90, 130)
f.step(120, 200, update_estimation=True)
f.print_states()
f.plot()
