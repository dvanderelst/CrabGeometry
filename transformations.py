import math

# dx, dy, dtheta: location and orienation of frame in world
# wx, wy a point in the world, to be transformed to the frame
def world2frame(wx, wy, dx, dy, dtheta):
    cos = math.cos(math.radians(dtheta))
    sin = math.sin(math.radians(dtheta))
    x_translated = wx - dx
    y_translated = wy - dy
    new_x = cos * x_translated + sin * y_translated
    new_y = -sin * x_translated + cos * y_translated
    return new_x, new_y


# dx, dy, dtheta: location and orienation of frame in world
# fx, fy a point in the frame, to be transformed to the world
def frame2world(fx, fy, dx, dy, dtheta):
    cos_rot = math.cos(math.radians(-dtheta))
    sin_rot = math.sin(math.radians(-dtheta))
    new_x = cos_rot * fx + sin_rot * fy + dx
    new_y = -sin_rot * fx + cos_rot * fy + dy
    return new_x, new_y

if __name__ == "__main__":
    dx = 10
    dy = 10
    drot = 90

    # result = world2frame(0, 0, dx, dy, drot)
    # print(result)
    #
    result = frame2world(10,10,dx, dy, drot)
    print(result)