import numpy as np
import matplotlib.pyplot as plt
from functions import Transform
from functions import render_object

"""
For each affine transformation, I create a new object of the Transform class. 
I do this because all successive transformations accumulate in the mat matrix, 
so in steps 2 and 3, instead of just translation t_1 and t_2 respectively, 
we would also have an additional rotation (with rotation matrix R from step 1).
"""


# Load data from the given file
extracted_info = np.load("hw2.npy", allow_pickle=True)[()]

# Extract data from the dictionary
v_pos = np.array(extracted_info['v_pos'])
v_clr = np.array(extracted_info['v_clr'])
t_pos_idx = np.array(extracted_info['t_pos_idx'])
eye = np.array(extracted_info['eye'])
target = np.array(extracted_info['target'])
up = np.array(extracted_info['up'])
t_0 = np.array(extracted_info['t_0'])
t_1 = np.array(extracted_info['t_1'])
rot_axis_0 = np.array(extracted_info['rot_axis_0'])
theta_0 = np.array(extracted_info['theta_0'])
res_w = extracted_info['res_w']
res_h = extracted_info['res_h']
plane_w = extracted_info['plane_w']
plane_h = extracted_info['plane_h']
focal = extracted_info['focal']

print("Step 0 in progress...")
# Render the object and display/save the first image
img_array = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
plt.imshow(img_array)
plt.title('first image')
plt.show()
plt.imsave('0.jpg', np.array(img_array))
print("Step 0 completed successfully!\n")

print("Step 1 in progress...")
# Create and apply affine transformation for rotation
affine_transform_object1 = Transform()
affine_transform_object1.rotate(theta_0, rot_axis_0)
v_pos = affine_transform_object1.transform_pts(v_pos)

# Render the object after rotation and display/save the image
img_array = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
plt.imshow(img_array)
plt.title('Rotation by angle theta around an axis parallel to rot_axis')
plt.show()
plt.imsave('1.jpg', np.array(img_array))
print("Step 1 completed successfully!\n")

print("Step 2 in progress...")
# Create and apply affine transformation for translation (t_1)
affine_transform_object2 = Transform()
affine_transform_object2.translate(t_0)
v_pos = affine_transform_object2.transform_pts(v_pos)

# Render the object after the first translation and display/save the image
img_array = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
plt.imshow(img_array)
plt.title('Translation by t_1')
plt.show()
plt.imsave('2.jpg', np.array(img_array))
print("Step 2 completed successfully!\n")

print("Step 3 in progress...")
# Create and apply affine transformation for translation (t_2)
affine_transform_object3 = Transform()
affine_transform_object3.translate(t_1)
v_pos = affine_transform_object3.transform_pts(v_pos)

# Render the object after the second translation and display/save the image
img_array = render_object(v_pos, v_clr, t_pos_idx, plane_h, plane_w, res_h, res_w, focal, eye, up, target)
plt.imshow(img_array)
plt.title('Translation by t_2')
plt.show()
plt.imsave('3.png', np.array(img_array))
print("Step 3 completed successfully!")

