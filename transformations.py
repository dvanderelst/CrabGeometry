import math

# fx, fy, ftheta: location and orienation of frame in world
# x, y a point in the world, to be transformed to the frame
def world2frame(x, y, fx, fy, ftheta):
    cos = math.cos(math.radians(-ftheta))
    sin = math.sin(math.radians(-ftheta))
    x_translated = x - fx
    y_translated = y - fy
    new_x = cos * x_translated + sin * y_translated
    new_y = -sin * x_translated + cos * y_translated
    return new_x, new_y


# fx, fy, ftheta: location and orienation of frame in world
# x, y a point in the frame, to be transformed to the world
def frame2world(x, y, fx, fy, ftheta):
    cos_rot = math.cos(math.radians(ftheta))
    sin_rot = math.sin(math.radians(ftheta))
    new_x = cos_rot * x + sin_rot * y + fx
    new_y = -sin_rot * x + cos_rot * y + fy
    return new_x, new_y

if __name__ == "__main__":
    fx = 10
    fy = 10
    rot = -90

    result = frame2world(10, 10, fx, fy, rot)
    print(result)

    result = world2frame(0, 0, fx, fy, rot)
    print(result)