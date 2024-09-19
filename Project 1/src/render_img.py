from f_shading import f_shading
from g_shading import g_shading

"""
render_img function : 

img is a colored image of dimensions M × N × 3.
The image will contain K colored triangles projecting a 3D object onto 2 dimensions.

faces is a K × 3 array containing the vertices of K triangles.
Each row of the array represents the three vertices of a triangle.
In the faces array, the coordinates of the vertices are not present.
Instead, each row of the faces array is a 1 × 3 vector,
where each element is an integer referring to the coordinates of a specific vertex in the vertices array
(the coordinates of the first vertex in the vertices array correspond to the number 0).

The L × 2 array vertices contains the coordinates of the vertices of all triangles in the image.
(It contains the coordinates of a total of L vertices).

The L × 3 array vcolors contains the colors of the vertices of all triangles in the image.
depth is the L × 1 array that indicates the depth of each vertex.
The variable shading takes the value "f" or "g" and determines the shading function (f_shading or g_shading).
"""


def render_img(faces, vertices, vcolors, depth, shading):
    # M = 512 = canvas height  ,  N = 512 = canvas width
    img = []
    # I create the canvas.
    for i in range(512):
        img.append([])
        for j in range(512):
            img[i].append([])
            # The background of the canvas is white.
            img[i][j] = [1, 1, 1]
    updated_img = img.copy()
    t_colors = []  # contains the color (i.e., a 1x3 vector) of each vertex of a triangle.
    # Each element in a row of the t_colors array is a 1x3 vector. Each row refers to one triangle.
    # Therefore, a row of the t_colors array has the following format: [[1x3 vector], [1x3 vector], [1x3 vector]].

    t_depths = []  # It contains the depths of the triangles.
    info1 = []  # In this list, I save the arrays t_depths and t_colors.
    info2 = []  # In this list, I save the arrays t_depths and faces.

    for i in range(len(faces)):
        # vcolors[faces[i][0]] --> It provides the color vector of the 'faces[i][0]' vertex (faces[i][0] is an integer).
        t_colors.append([vcolors[faces[i][0]], vcolors[faces[i][1]], vcolors[faces[i][2]]])
        # depth[faces[i][0]] --> It provides the depth of the 'faces[i][0]' vertex
        # The depth of a triangle is calculated as the centroid of the depths of its vertices.
        t_depths.append((depth[faces[i][0]] + depth[faces[i][1]] + depth[faces[i][2]]) / 3)
        # The first element of each row of the info1 array represents the depth of a triangle.
        info1.append([t_depths[i], t_colors[i]])
        for j in range(3):
            # The element faces[i][j] is no longer equal to an integer k.
            # Instead, it equals the coordinates of the k-th vertex of the vertices array.
            faces[i][j] = vertices[faces[i][j]]

        # The first element of each row of the info2 array represents the depth of a triangle.
        info2.append([t_depths[i], faces[i]])

    # I am performing descending sorting with respect to the first element of each row of the array info1.
    info1.sort(reverse=True, key=lambda k: k[0])
    # I am performing descending sorting with respect to the first element of each row of the array info2.
    info2.sort(reverse=True, key=lambda k: k[0])
    # Thus, I ensured that the depths are sorted from largest to smallest in the arrays info1 and info2.
    # Also, the color vectors and vertices coordinates of the triangles were sorted based on their corresponding depth.

    # I store the depths of the triangles, the color vectors, and the vertices coordinates in their new sorted order.
    new_t_depths, new_t_colors, new_faces = [], [], []
    for elem in info1:
        new_t_depths.append(elem[0])
        new_t_colors.append(elem[1])
    for elem in info2:
        new_faces.append(elem[1])

    if shading != "f" and shading != "g":
        print('An error occurred: shading must be "f" or "g"')
        return 1
    elif shading == "f":
        for face in new_faces:
            index = 0
            for j in new_faces:
                # Find the index of the "face" in the new_faces array.
                # "face" is a list containing the 2D coordinates of the 3 vertices of a triangle.
                if face != j:
                    index += 1
                else:
                    break
            updated_img = f_shading(img, face, new_t_colors[index])
    elif shading == "g":
        for face in new_faces:
            index = 0
            for j in new_faces:
                # Find the index of the "face" in the new_faces array.
                # "face" is a list containing the 2D coordinates of the 3 vertices of a triangle.
                if face != j:
                    index += 1
                else:
                    break
            updated_img = g_shading(img, face, new_t_colors[index])

    return updated_img
