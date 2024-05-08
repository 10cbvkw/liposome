import torch
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator

# Set up the SAM model and mask generator
def setup_sam_model(model_type="vit_h", checkpoint_path="sam_vit_h_4b8939.pth"):
    sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
    mask_generator = SamAutomaticMaskGenerator(sam)
    return mask_generator

# Function to generate masks
def generate_masks(image, mask_generator):
    masks = mask_generator.generate(image)
    return masks

# Function to calculate the radius of each mask
def calculate_radius(mask, center):
    y_indices, x_indices = np.where(mask)
    distances = np.sqrt((x_indices - center[0])**2 + (y_indices - center[1])**2)
    return np.max(distances)

# Function to calculate roundness
def is_round_enough(mask, center, radius, threshold=0.9):
    mask_area = np.sum(mask)
    circle_area = np.pi * (radius**2)
    return mask_area >= threshold * circle_area

# Function to save round masks and their information
def save_round_masks(image, masks, image_name, output_dir, threshold=0.9, min_radius=100):
    # Create an empty mask for display
    mask_display = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    # Apply each mask with a different color and calculate its center and radius
    centers_and_radii = []
    for i, mask in enumerate(masks):
        color = np.random.randint(0, 255, (1, 3)).tolist()[0]

        # Calculate the center of the mask
        moments = cv2.moments(mask['segmentation'].astype(np.uint8))
        if moments['m00'] != 0:
            center_x = int(moments['m10'] / moments['m00'])
            center_y = int(moments['m01'] / moments['m00'])
            center = (center_x, center_y)

            # Calculate the radius
            radius = calculate_radius(mask['segmentation'], center)

            # Check if the mask is round enough and larger than the minimum radius
            if is_round_enough(mask['segmentation'], center, radius, threshold) and radius >= min_radius:
                centers_and_radii.append((center, radius))

                # Draw the center as a circle on the original image
                cv2.circle(mask_display, center, 5, (255, 255, 255), -1)
                # Draw the radius as a circle
                cv2.circle(mask_display, center, int(radius), (255, 255, 255), 2)
                mask_display[mask['segmentation']] = color

    # Overlay the masks on the original image
    overlaid_image = cv2.addWeighted(image, 0.6, mask_display, 0.4, 0)

    # Save the overlaid image
    output_image_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}_round_masks.png")
    plt.imsave(output_image_path, overlaid_image)

    # Save the centers and radii to a text file
    output_text_path = os.path.join(output_dir, f"{os.path.splitext(image_name)[0]}_centers_and_radii.txt")
    with open(output_text_path, 'w') as file:
        for idx, (center, radius) in enumerate(centers_and_radii):
            file.write(f"Round Mask {idx + 1}: Center = {center}, Radius = {radius:.2f}\n")

# Load and preprocess image
def load_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# Process all images in a directory
def process_images_in_directory(input_dir, output_dir, mask_generator, threshold=0.9, min_radius=100):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process each image in the input directory
    for image_name in os.listdir(input_dir):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, image_name)
            image = load_image(image_path)
            masks = generate_masks(image, mask_generator)
            save_round_masks(image, masks, image_name, output_dir, threshold, min_radius)

# Example usage
if __name__ == "__main__":
    # Download SAM model checkpoint from GitHub - facebookresearch/segment-anything: The repository provides code for running inference with 
    sam_checkpoint_path = "sam_vit_h_4b8939.pth"  # Path to your checkpoint file
    input_dir = "images"  # Path to the folder containing input images
    output_dir = "output"  # Path to the folder for saving results

    # Set up the SAM model and mask generator
    mask_generator = setup_sam_model(checkpoint_path=sam_checkpoint_path)

    # Process all images in the input directory and save results
    process_images_in_directory(input_dir, output_dir, mask_generator, threshold=0.8, min_radius=90)