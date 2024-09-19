"""
line_drawing function :

Τhe line_drawing function implements bresenham's algorithm for drawing lines.
Takes as input the coordinates (x,y) of the points vert1, vert2.
vert1 is the start point of the line and vert2 is the end point of the line I want to draw.
The function returns a list containing the coordinates of all points of the line.
"""


def line_drawing(vert1, vert2):
    x1 = vert1[0]
    y1 = vert1[1]
    x2 = vert2[0]
    y2 = vert2[1]
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    slope = dy > dx

    if slope:  # Ιf (dy>dx) is true, i.e. the slope is greater than 1.
        # To make the slope smaller than 1 I have to rotate the coordinate system.
        # So the new value of x will be the old value of y and the new value of y will be the old value of x.
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:  # If vert1 is further right than vert2,
        # then vert2 is the beginning of the line and vert1 is the end of the line.
        # So I have to swap their coordinates.
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    # I apply bresenham's algorithm
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    f = -2 * dy + dx
    y = y1
    ystep = 1 if y1 < y2 else -1  # If y1 < y2, then vert2 is located higher than vert1.
    # Therefore the slope of the line is upward and ystep = +1.
    # Otherwise, the slope of the line is downward and ystep = -1.

    points = []  # Ιn this list I store all the points of the line.
    for x in range(x1, x2 + 1):
        coord = [y, x] if slope else [x, y]
        points.append(coord)
        if f < 0:
            y += ystep
            f = f - 2 * (dy - dx)
        else:
            f = f - 2 * dy
    return points
