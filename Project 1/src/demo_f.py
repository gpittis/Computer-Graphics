import numpy as np
import matplotlib.pyplot as plt
import cv2
from render_img import render_img

# Load the input data from the file hw1.npy
extracted_info = np.load('hw1.npy', allow_pickle=True)[()]
# Extract lists from the dictionary
faces = extracted_info['faces'].tolist()
vertices = extracted_info['vertices'].tolist()
vcolors = extracted_info['vcolors'].tolist()
depth = extracted_info['depth'].tolist()

print("Image filling in progress...")
img = render_img(faces, vertices, vcolors, depth, "f")


# Save the final image using the matplotlib library.

# Display the image
plt.imshow(img)
plt.title('f_shading')
plt.show()
# Save the image
plt.imsave('f_shading_matplotlib.png', np.array(img))


# Save the final image using the OpenCV library.

"""
I convert the img from floating-point values in the range [0, 1] to integers in the range [0, 255], 
which is the typical range for pixel values in an 8-bit per channel image. 
Then, I convert the data type of the array to uint8 (unsigned 8-bit integer).
"""
#img = (np.array(img) * 255).astype(np.uint8)

# Convert color space from RGB to BGR
#img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
# Display the image
#cv2.imshow('Image', img_BGR)
#cv2.waitKey(0)  # Waits for a key event in a window created by OpenCV.
#cv2.destroyAllWindows()  # Closes all the windows created by OpenCV in order to release system resources.
# Save the image
#cv2.imwrite('F_SHADING_OpenCV.png', img_BGR)
