import math
from matplotlib import pyplot
import numpy




# xy in a frame 1 to a frame 2 whose origin lies at dx,dy in frame 1 and rotated by rot
def convert_tr(x, y, dx, dy, rot):
    cos_rot = math.cos(math.radians(rot))
    sin_rot = math.sin(math.radians(rot))
    x_translated = x - dx
    y_translated = y - dy
    x_rotated = cos_rot * x_translated + sin_rot * y_translated
    y_rotated = -sin_rot * x_translated + cos_rot * y_translated
    return x_rotated, y_rotated


# xy in a frame 1 to a frame 2 whose origin lies at dx,dy in frame 1 and rotated by rot
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

# a = Frame()
# a.step(0,100)
# a.step(90,100)
# a.step(130,100)
# a.plot()
#
#
# print(a.world2frame(100,230))
# print(a.frame2world(130,0))

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
        dx, dy = self.real_frame.world2frame(0,0)
        x,y = self.estimated_frame.frame2world(dx, dy)
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

        pyplot.figure()
        real_history = self.real_frame.history
        n = real_history.shape[0]
        ones = numpy.ones(n)
        pyplot.plot(real_history[:, 0], real_history[:, 1], 'k',linewidth=2, alpha=0.5)
        pyplot.quiver(real_history[:, 0], real_history[:, 1], ones, ones, angles=real_history[:, 2], zorder=100,color='r', )
        pyplot.quiver(real_history[:, 0], real_history[:, 1], ones, ones, angles=real_history[:, 2]+90, zorder=100,color='g')
        pyplot.scatter(0, 0, color='k', s=100, alpha=0.5)
        pyplot.title('Real')
        pyplot.grid()
        ax = pyplot.gca()
        ax.set_aspect('equal', 'box')

        pyplot.figure()
        estimated_history = self.estimated_frame.history
        n = estimated_history.shape[0]
        ones = numpy.ones(n)
        pyplot.plot(estimated_history[:, 0], estimated_history[:, 1], 'k', linewidth=2, alpha=0.5)
        pyplot.quiver(estimated_history[:, 0], estimated_history[:, 1], ones, ones, angles=estimated_history[:, 2], zorder=100, color='r', )
        pyplot.quiver(estimated_history[:, 0], estimated_history[:, 1], ones, ones, angles=estimated_history[:, 2] + 90, zorder=100, color='g')
        x, y = self.estimated_burrow_location()
        pyplot.scatter(x, y, color='k', s=100, alpha=0.5)
        pyplot.title('Estimated')
        pyplot.grid()
        ax = pyplot.gca()
        ax.set_aspect('equal', 'box')
        pyplot.show()





# def plot_history(history, color):
#     n = history.shape[0]
#     ones = numpy.ones(n)
#     pyplot.plot(history[:, 0], history[:, 1], color, alpha=0.5)
#     pyplot.quiver(history[:, 0], history[:, 1], ones, ones, angles=history[:, 2], zorder=100,color='r', )
#     pyplot.quiver(history[:, 0], history[:, 1], ones, ones, angles=history[:, 2]+90, zorder=100,color='g')
# f = Crab()
# f.step(0, 130)
# f.step(90, 130)
# f.step(120, 200, update_estimation=True)
# f.print_states()
# f.plot()
