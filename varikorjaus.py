import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import os

def correct_colors(image_path, output_path, new_white_point=(254, 254, 254), margin=250):
    # Load the image using PIL to handle .tif format properly
    image = Image.open(image_path)
    image = np.array(image)

    # If the image has multiple layers (e.g., RGBA), just use the RGB channels
    if image.shape[-1] == 4:
        image = image[:, :, :3]

    # Convert the image to RGB if it is not already
    if len(image.shape) == 2 or image.shape[-1] == 1:  # Grayscale to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image_rgb = image

    # Get image dimensions
    height, width, _ = image_rgb.shape

    # Find the darkest point in the central part of the image (excluding margins)
    reshaped_image = image_rgb[margin:height-margin, margin:width-margin].reshape((-1, 3))
    darkest_point = np.min(reshaped_image, axis=0).astype(np.float32)

    # Find the lightest point in the specified margins, excluding near-white pixels
    margin_pixels = image_rgb[margin:height-margin, margin:width-margin].reshape(-1, 3)
    valid_pixels = margin_pixels[np.all(margin_pixels < [247, 220, 185], axis=1)]
    if valid_pixels.size == 0:
        raise ValueError("No valid pixels found that are not near-white.")
    lightest_point = np.max(valid_pixels, axis=0).astype(np.float32)

    # Print the darkest and lightest colors
    print(f'Darkest point: {darkest_point}')
    print(f'Lightest point: {lightest_point}')

    # Normalize the colors to the range [0, 1]
    normalized = (image_rgb.astype(np.float32) - darkest_point) / (lightest_point - darkest_point)
    normalized = np.clip(normalized, 0, 1)

    # Scale to the new white point
    new_white_point_array = np.array(new_white_point, dtype=np.float32)
    corrected = normalized * new_white_point_array
    corrected = np.clip(corrected, 0, 255).astype(np.uint8)

    # Save the adjusted image
    adjusted_image_pil = Image.fromarray(corrected)
    adjusted_image_pil.save(output_path)
    return output_path

def process_images(input_folder, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.tif', '.jpg', '.png', '.jpeg')):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, 'corrected_' + filename)
            try:
                corrected_image_path = correct_colors(input_image_path, output_image_path)
                print(f'Corrected image saved at {corrected_image_path}')
            except Exception as e:
                print(f'Error processing {input_image_path}: {e}')

input_folder = '/Users/joeltikkanen/Documents/lsb/kaanto_output'
output_folder = '/Users/joeltikkanen/Documents/lsb/output'
process_images(input_folder, output_folder)
