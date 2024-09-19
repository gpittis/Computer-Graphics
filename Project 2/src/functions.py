import numpy as np
from render_img import render_img

# Note: The numbers of the equations referred to in the comments can be found in the course notes (gr-notes.pdf)

"""
The class Transform contains as an attribute the matrix mat(4χ4), which represents an affine transform and 
is initialized to the identity matrix I4. 

The rotate function calculates the rotation matrix corresponding to a clockwise rotation by an angle theta 
about an axis defined by the unit vector u and then updates the mat matrix. 
Then the mat matrix represents a rotation transform. 

The translate function updates the mat matrix with the translation vector t. 
Then the mat matrix represents a translation transform. 

The transform_pts function applies the transformation matrix mat to the 3D points of the pts array it takes as input.
"""


class Transform:
    def __init__(self):  # Constructor of the class
        # mat is the transformation matrix in homogeneous coordinates.
        self.mat = np.identity(4)  # Initialization to I4

    def rotate(self, theta, u):
        # I calculate the elements of the non-homogeneous rotation matrix R (equation 5.45 )
        # R is a 3x3 array
        # r1 is the first row of the matrix R
        r1 = np.array([(1 - np.cos(theta)) * u[0] ** 2 + np.cos(theta),
                       (1 - np.cos(theta)) * u[0] * u[1] - np.sin(theta) * u[2],
                       (1 - np.cos(theta)) * u[0] * u[2] + np.sin(theta) * u[1]])
        # r2 is the second row of the matrix R
        r2 = np.array([(1 - np.cos(theta)) * u[1] * u[0] + np.sin(theta) * u[2],
                       (1 - np.cos(theta)) * u[1] ** 2 + np.cos(theta),
                       (1 - np.cos(theta)) * u[1] * u[2] - np.sin(theta) * u[0]])
        # r3 is the third row of the matrix R
        r3 = np.array([(1 - np.cos(theta)) * u[2] * u[0] - np.sin(theta) * u[1],
                       (1 - np.cos(theta)) * u[2] * u[1] + np.sin(theta) * u[0],
                       (1 - np.cos(theta)) * u[2] ** 2 + np.cos(theta)])

        # I appropriately update the transformation matrix mat with the rotation matrix R according to equation 5.49
        self.mat[0][0] = r1[0]
        self.mat[0][1] = r1[1]
        self.mat[0][2] = r1[2]

        self.mat[1][0] = r2[0]
        self.mat[1][1] = r2[1]
        self.mat[1][2] = r2[2]

        self.mat[2][0] = r3[0]
        self.mat[2][1] = r3[1]
        self.mat[2][2] = r3[2]

    def translate(self, t):
        # t is the translation vector in non-homogeneous coordinates.
        # I appropriately update the transformation matrix mat with the translation vector t according to equation 5.37
        self.mat[0][3] = t[0]
        self.mat[1][3] = t[1]
        self.mat[2][3] = t[2]

    def transform_pts(self, pts):
        # pts is a 3xN array
        # I add 1 to each column of the pts matrix, thus changing its dimensions to 4xN.
        # In this way, I can transform the 3D points of the pts matrix based on the mat matrix.

        modified_cols = []  # Initialize an empty list to store the modified columns
        for vector in pts.T:

            # The vector is a column vector in pts array
            # Convert the column vector to a list and append 1 to the end (making it homogeneous)
            modified_col = vector.tolist() + [1]

            # Append the modified column to the list of modified columns
            modified_cols.append(modified_col)

        # Convert the list of modified columns to a NumPy array
        pts_transpose = np.array(modified_cols)  # pts_transpose is a Nx4 array
        pts = pts_transpose.T

        pts_transform = np.dot(self.mat, pts)  # Apply the affine transformation to the points of pts array
        # pts_transform is a 4xN array

        rows, cols = pts_transform.shape  # Get the number of rows and columns of pts_transform

        # I want to convert the coordinates of the transformed points to non-homogeneous
        # I initially create an empty 3xN array
        new_pts_transform = np.empty((rows - 1, cols))

        # Copy the rows of pts_transform except the last one to new_pts_transform
        for i in range(rows - 1):
            new_pts_transform[i] = pts_transform[i]

        # Update the pts_transform with the non-homogeneous coordinates (pts_transform is now a 3xN array)
        pts_transform = new_pts_transform
        return pts_transform


"""
The function  world2view transforms the input points pts into the coordinate system of the camera.
pts is a 3xN array.
R is a 3x3 rotation matrix representing the transformation of the new coordinate system with respect to the original one.
c0 is a 1x3 vector representing the reference point of the new coordinate system with respect to the original one.
The function returns the Nχ3 array pts_transform containing the transformed points pts.
"""


def world2view(pts, R, c0):
    # I use pts.T so that subtraction is feasible since c0 is a 1χ3 vector
    pts_new = pts.T - c0  # Translate the input points by c0 and store them in the array pts_new
    # pts_new is a Nx3 array

    pts_transform = np.dot(R, pts_new.T).T  # Transform the points using the rotation matrix R
    # pts_transform is a Nx3 array

    return pts_transform


"""
The function lookat computes the 3x3 rotation matrix R and the 1x3 translation vector t, 
which are needed for transforming points from the World Coordinate System (WCS) to the camera coordinate system.
The function returns the rotation matrix R and the translation vector t.

eye is a 3x1 vector representing the camera center.
up is a 3x1 unit vector representing the camera's up direction.
target is a 3x1 vector representing the target point (the point where the camera is aiming).
"""


def lookat(eye, up, target):

    # Convert the vectors from 3x1 to 1x3 format
    eye = eye.flatten()
    up = up.flatten()
    target = target.flatten()

    ck = target - eye  # The vector ck is the axis of the camera lens
    norm_ck = np.sqrt(ck[0] ** 2 + ck[1] ** 2 + ck[2] ** 2)  # Calculate the norm of the vector ck

    # c_x, c_y, c_z are the coordinates of the unit vectors of the camera with respect to the WCS

    c_z = ck / norm_ck  # Calculate c_z (equation 6.6)
    # Therefore, the axis of the lens is defined by the unit vector c_z

    dot_product = np.dot(up, c_z)  # The inner product <u, c_z> in equation 6.7
    # The vector v is parallel to the unit vector of the y-axis. I use it to find c_y
    v = up - dot_product * c_z  # equation 6.7
    norm_v = np.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)  # Calculate the norm of the vector t
    c_y = v / norm_v  # Calculate c_y (equation 6.7)

    # Compute the cross product of c_y and c_z. In this way I calculate c_x (equation 6.8)
    c_x = np.array([c_y[1] * c_z[2] - c_y[2] * c_z[1],
                    c_y[2] * c_z[0] - c_y[0] * c_z[2],
                    c_y[0] * c_z[1] - c_y[1] * c_z[0]])

    # I use the unit vectors (c_x, c_y, c_z) to calculate the 3x3 rotation matrix R (equation 6.11)
    r_transpose = np.array([c_x, c_y, c_z])
    R = r_transpose.T

    t = eye  # Set the translation vector t (equation 6.12)
    return R, t


"""
The function perspective_project computes the perspective projections and the depth of the input points pts
and then returns them. 
Essentially, I use the x and y coordinates of the input points to generate their perspective projections. 
Additionally, the z coordinate of the input points represents their depth.

pts is the 3xN matrix of input points.
focal represents the distance from the camera's focal point to its center.
R is the 3χ3 rotation matrix to the camera's coordinate system.
t is the 1x3 translation vector to the camera's coordinate system.
"""


def perspective_project(pts, focal, R, t):
    # Transform the input points to camera's coordinates
    # pts_transform is a Nx3 array
    pts_transform = world2view(pts, R, t)

    # Extracting the z-coordinate (i.e., the third coordinate) to create the depths array
    depths = []
    for point in pts_transform:
        depths.append(point[2])  # The z-coordinate represents the depth of the points
    depths = np.array(depths)  # depths is a 1-D array

    # Initialize lists to store the projected x and y coordinates
    x_q = []
    y_q = []

    # Below, I apply the relationships: x_q = (w * x_p)/z_p , y_q = (w * y_p)/z_p  (page 72 of gr-notes.pdf)
    # focal corresponds to w
    # z_p corresponds to depths[i]
    # x_p corresponds to pts_transform[i][0]
    # y_p corresponds to pts_transform[i][1]
    # Here, I'm working with non-homogeneous coordinates instead of homogeneous ones, as on page 72
    for i in range(len(depths)):
        # Calculate the projected x coordinate
        x_q.append((focal / depths[i]) * pts_transform[i][0])
        # Calculate the projected y coordinate
        y_q.append((focal / depths[i]) * pts_transform[i][1])
    x_q = np.array(x_q)
    y_q = np.array(y_q)

    pts_2d = np.array([x_q, y_q])  # pts_2d is a 2xN array
    # The first row of the array pts_2d represents the x-projections, while the second row represents the y-projections.

    # The Nx2 array pts_2d.T contains the 2D coordinates of the input points in the camera's image plane.
    return pts_2d.T, depths


"""
The function rasterize maps the coordinates of input points from the camera's plane coordinate system, 
with a plane of dimensions plane_h × plane_w, to integer positions (pixels) of an image with dimensions res_h × res_w.
The function returns the rasterized points.
"""


def rasterize(pts_2d, plane_w, plane_h, res_w, res_h):
    # Initialize a zero-filled array to store the rasterized points
    pts_rast = np.zeros_like(pts_2d)
    scale_x = res_w / plane_w
    scale_y = res_h / plane_h
    for i in range(len(pts_2d)):
        # Calculate the x-coordinate of the rasterized point
        pts_rast[i][0] = np.around((pts_2d[i][1] + plane_w / 2) * scale_x)
        # Calculate the y-coordinate of the rasterized point
        pts_rast[i][1] = np.around((pts_2d[i][0] + plane_h / 2) * scale_y)
    return pts_rast


"""
The function render_object captures a 3D scene of an object from a camera. 
It returns an array of size resh × resw × 3 (the photograph of the object).
Also, implements the entire rendering pipeline of the object. 
Additionally, it colors the object using the Gouraud shading method.

v_pos array (3xN) represents the three-dimensional coordinates of the object's points.
v_clr array (Nx3) is the matrix containing the colors of the vertices.
t_pos_idx array (Fx3) contains indices pointing to points in the v_pos that constitute the vertices of the triangles.
plane_h is the height of the camera's plane.
plane_w is the width of the camera's plane.
res_h is the height of the canvas in pixels.
res_w is the width of the canvas in pixels.
focal represents the distance from the camera's focal point to its center.
eye (3x1 vector) is the center of the camera with respect to the WCS.
up (3x1 vector) is the up vector of the camera.
target (3x1 vector) is the target point of the camera.
"""


def render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target):
    # Compute the rotation matrix and translation vector
    R, t = lookat(eye, up, target)

    # Project the 3D points to 2D and calculate their depths
    pts_2d, depths = perspective_project(v_pos, focal, R, t)

    # Rasterize the projected points
    pts_rast = rasterize(pts_2d, plane_w, plane_h, res_w, res_h)

    # Convert data to lists
    pts_rast_list = []
    for row in pts_rast:
        pts_rast_row = []
        for point in row:
            pts_rast_row.append(int(point))
        pts_rast_list.append(pts_rast_row)

    depths_list = []
    for depth in depths:
        depths_list.append(depth)

    t_pos_idx_list = []
    for row in t_pos_idx:
        t_pos_idx_row = []
        for value in row:
            t_pos_idx_row.append(value)
        t_pos_idx_list.append(t_pos_idx_row)

    v_clr_list = []
    for color in v_clr:
        v_clr_row = []
        for c in color:
            v_clr_row.append(c)
        v_clr_list.append(v_clr_row)

    # Render the image
    image_array = render_img(t_pos_idx_list, pts_rast_list, v_clr_list, depths_list, "g")

    return image_array  # Return the rendered image
