import os
import mrcfile
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def mrc_to_jpg(mrc_path, jpg_path):
    # Open the MRC file
    with mrcfile.open(mrc_path, permissive=True) as mrc:
        img_data = mrc.data

    # Normalize the image data to scale from 0 to 255
    normalized_img = (img_data - np.min(img_data)) / (np.max(img_data) - np.min(img_data))
    image_8bit = (normalized_img * 255).astype(np.uint8)

    # Create an image and save as JPEG
    image = Image.fromarray(image_8bit)
    image.save(jpg_path)
    print(f"Image saved as {jpg_path}")

    # Optionally display the image
    # plt.imshow(image_8bit, cmap='gray')
    # plt.title('CryoEM Image')
    # plt.axis('off')  # Turn off axis numbers and ticks
    # plt.show()

# Example usage
image_path = '/home/pc/Desktop/liposome/images'
if not os.path.exists(image_path):
            os.makedirs(image_path)

for i in range(1, 10):
    mrc_path = '/home/pc/Desktop/liposome/stack_2nd_010'+str(i)+'_DW.mrc'  # Path to your MRC file
    jpg_path = image_path + '/stack_2nd_010'+str(i)+'_DW.jpg'  # Desired output path for the JPEG file
    mrc_to_jpg(mrc_path, jpg_path)
