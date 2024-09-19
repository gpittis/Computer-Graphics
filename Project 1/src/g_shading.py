import numpy as np
from line_drawing import line_drawing
from vector_interp import vector_interp
"""
g_shading:

The function g_shading has the same input arguments as the function f_shading.
In this function, I use the vector_interp function to color the pixels of the triangles.
"""


def g_shading(img, vertices, vcolors):

    # The correct rendering of the image's fish is achieved by reversing the x-coordinates of the triangle vertices.
    # Otherwise, the fish will appear "upside down".
    vertices = np.array(vertices)
    vertices[0][0] = -vertices[0][0]
    vertices[1][0] = -vertices[1][0]
    vertices[2][0] = -vertices[2][0]

    # The coordinates of the vertices of the triangle.
    p1 = vertices[2]
    p2 = vertices[1]
    p3 = vertices[0]

    # The distance of each side's x-coordinates.
    dx1 = abs(p1[0] - p3[0])
    dx2 = abs(p1[0] - p2[0])
    dx3 = abs(p3[0] - p2[0])

    # The distance of each side's y-coordinates.
    dy1 = abs(p1[1] - p3[1])
    dy2 = abs(p1[1] - p2[1])
    dy3 = abs(p3[1] - p2[1])

    # The sides of the triangle.
    side1 = line_drawing(p1, p3)
    side2 = line_drawing(p1, p2)
    side3 = line_drawing(p3, p2)
    sides = [side1, side2, side3]  # In this list, I store the sides of the triangle.

    # The colors of the vertices of the triangle.
    p1_color = np.array(vcolors[2])
    p2_color = np.array(vcolors[1])
    p3_color = np.array(vcolors[0])

    info = []  # In this list, I will store the x_max, x_min, y_max, y_min of each side of the triangle ( 3x4 list).
    sub_coord = []  # In this list, I store all the y-coordinates of one side of the triangle.

    for side in sides:
        coord_x_max = max(side)
        coord_x_min = min(side)
        x_max = coord_x_max[0]  # The maximum x-coordinate of one side of the triangle.
        x_min = coord_x_min[0]  # The minimum x-coordinate of one side of the triangle.
        for i in side:
            sub_coord.append(i[1])
        y_max = max(sub_coord)  # The maximum y-coordinate of one side of the triangle.
        y_min = min(sub_coord)  # The minimum y-coordinate of one side of the triangle.
        sub_coord = []
        elem = [x_max, x_min, y_max, y_min]
        info.append(elem)

    # I calculate the x_max, x_min, y_max, y_min of the triangle.
    y_max = max(np.array([info[0][2], info[1][2], info[2][2]]))
    y_min = min(np.array([info[0][3], info[1][3], info[2][3]]))
    x_max = max(np.array([info[0][0], info[1][0], info[2][0]]))
    x_min = min(np.array([info[0][1], info[1][1], info[2][1]]))

    active_points_counter = 0  # Number of active points encountered.

    for y in range(y_min, y_max + 1):
        # For each y-coordinate of the triangle, I create a scanline.
        # This scanline is large enough to scan all the triangle pixels located at that y-coordinate.
        scan_line = line_drawing([x_min, y], [x_max, y])
        active_points = []  # The list in which I store the coordinates of the active points.

        # In this for loop, I'm coloring the outline (i.e., the sides) of the triangle.
        for j in scan_line:
            if j in side1:  # If the j-th point of the scan line exists on the side "side1" of the triangle.
                if dy1 > dx1:  # Then if the slope of this side is greater than 1.
                    # So, I provide the y-coordinate of the point p ( j[1] ) to calculate its color.
                    # For this reason I have input argument dim = 2.
                    img[j[0]][j[1]] = vector_interp(p1, p3, p1_color, p3_color, j[1], 2)
                else:
                    # Otherwise, I provide the χ-coordinate of the point p ( j[0] ) to calculate its color.
                    # For this reason I have input argument dim = 1.
                    img[j[0]][j[1]] = vector_interp(p1, p3, p1_color, p3_color, j[0], 1)
            if j in side2:
                if dy2 > dx2:
                    img[j[0]][j[1]] = vector_interp(p1, p2, p1_color, p2_color, j[1], 2)
                else:
                    img[j[0]][j[1]] = vector_interp(p1, p2, p1_color, p2_color, j[0], 1)
            if j in side3:
                if dy3 > dx3:
                    img[j[0]][j[1]] = vector_interp(p3, p2, p3_color, p2_color, j[1], 2)
                else:
                    img[j[0]][j[1]] = vector_interp(p3, p2, p3_color, p2_color, j[0], 1)
            for k in sides:
                for i in k:

                    # If the i-th point of the k-th side of the triangle
                    # coincides with the j-th point of the scan line.
                    if i[1] == j[1] and i[0] == j[0]:
                        # Then add this point to the list of active points.
                        active_points.append(i)
                        # And increase the number of active points by 1.
                        active_points_counter += 1

        min_point = min(active_points)  # I find the active point with the minimum x-coordinate.
        max_point = max(active_points)  # I find the active point with the maximum x-coordinate.

        # If I haven't encountered a triangle vertex (active_points_counter != 1)
        if active_points_counter != 1:
            for i in range(min_point[0] + 1, max_point[0]):
                # Then I'm coloring the pixels that exist between the active points(i.e., pixels inside the triangle).
                # I'm NOT coloring the active points, because they were colored when I colored the triangle outline.
                img[i][y] = vector_interp(min_point, max_point, img[min_point[0]][y], img[max_point[0]][y], i, 1)
        active_points_counter = 0

    return img
