import numpy as np

"""
vector_interp function:

The vector_interp function takes as input the coordinates (p1[0],p1[1]) and (p2[0],p2[1]) of the points p1 and p2
and the color vector V1,V2 of each of these 2 points.
It also takes as input the x or y coordinate (coord) of a point p located on the line segment p1p2.
The choice of the coordinate of the point p depends on the value of the input argument dim
(dim = 1 means that coord = p[0] and dim = 2 means that coord = p[1]).
The function uses linear interpolation to calculate the vector color V of the point p and then returns it.
V1,V2,V are 1x3 vectors
p1,p2,p are 1x2 vectors
"""


def vector_interp(p1, p2, V1, V2, coord, dim):
    if dim == 1 and p2[0] != p1[0]:  # If p2[0] == p1[0], then l is not defined.
        l = (p2[0] - coord) / (p2[0] - p1[0])
        V = l * np.array(V1) + (1 - l) * np.array(V2)
    elif p2[0] == p1[0] and p2[1] == p1[1]:
        # The two points coincide, therefore I do not have a line segment p1p2.So slope l = 0
        V = np.array(V2)  # Or V == np.array(V1)
    if dim == 2 and p2[1] != p1[1]:  # If p2[1] == p1[1], then l is not defined.
        l = (p2[1] - coord) / (p2[1] - p1[1])
        V = l * np.array(V1) + (1 - l) * np.array(V2)
    elif p2[0] == p1[0] and p2[1] == p1[1]:
        # The two points coincide, therefore I do not have a line segment p1p2.So slope l = 0
        V = np.array(V2)  # Or V == np.array(V1)
    return V
