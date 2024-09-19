import numpy as np
from line_drawing import line_drawing
"""
f_shading function:

img is a 3D MxNx3 array with any pre-existing triangles (Μ = image height, N = image width).
In the third dimension of the img array are located the 1x3 color vectors of each pixel of the image.
The vertices is an 3 × 2 array and in each row contains the 2D coordinates of a vertex of the triangle.
The vcolors is a 3 × 3 array where each row contains the color of a vertex of the triangle as a 1x3 vector.
The elements of this 1x3 vector take values from 0 to 1.
"""


def f_shading(img, vertices, vcolors):

    # The coordinates of the vertices of the triangle.
    p1 = vertices[0]
    p2 = vertices[1]
    p3 = vertices[2]

    # The sides of the triangle.
    side1 = line_drawing(p1, p2)
    side2 = line_drawing(p2, p3)
    side3 = line_drawing(p3, p1)
    sides = [side1, side2, side3]  # In this list, I store the sides of the triangle.

    # The colors of the vertices of the triangle.
    p1_color = np.array(vcolors[0])
    p2_color = np.array(vcolors[1])
    p3_color = np.array(vcolors[2])

    # All triangle pixels will be colored with color equal to the vector average of the colors of the 3 vertices.
    pixel_color = (p1_color + p2_color + p3_color) / 3

    info = []  # In this list, I store the x_max, x_min, y_max, y_min of each side of the triangle ( 3x4 list).
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
        scan_line = sorted(line_drawing([x_min, y], [x_max, y]))
        active_points = []  # The list in which I store the coordinates of the active points.
        for j in scan_line:
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
            for i in range(min_point[0], max_point[0] + 1):
                # Then I'm coloring the pixels that exist between the active points(i.e., pixels inside the triangle).
                # I'm also coloring the active points themselves.
                img[i][y] = pixel_color
        active_points_counter = 0

    return img
