import cv2
import pytesseract
import numpy as np
from PIL import Image
import os

# Ensure TESSDATA_PREFIX is set correctly
os.environ["TESSDATA_PREFIX"] = "/Users/joeltikkanen/Documents/lsb/testdata"


def get_image_orientation(image_path):
    image = Image.open(image_path)
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Use pytesseract's OSD function to detect orientation
    osd = pytesseract.image_to_osd(cv_image, lang="fin")

    # Extract orientation
    rotation = int(osd.split("\n")[2].split(": ")[1])
    return rotation


def correct_image_orientation(image_path, output_path, rotation):
    image = Image.open(image_path)

    if rotation == 90:
        rotated_image = image.rotate(-90, expand=True)
    elif rotation == 180:
        rotated_image = image.rotate(180, expand=True)
    elif rotation == 270:
        rotated_image = image.rotate(90, expand=True)
    else:
        rotated_image = image

    rotated_image.save(output_path)
    print(f"Image saved correctly oriented: {output_path}")


# Directory containing the scanned images
input_directory = "/Users/joeltikkanen/Documents/lsb/input"
output_directory = "/Users/joeltikkanen/Documents/lsb/kaanto_output"

# Create output directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Find the first image and determine its orientation
image_files = sorted(
    [
        f
        for f in os.listdir(input_directory)
        if f.endswith(".tif") or f.endswith(".tiff")
    ]
)

if image_files:
    first_image_path = os.path.join(input_directory, image_files[0])
    base_rotation = get_image_orientation(first_image_path)
    print(f"Base rotation: {base_rotation}")

    # Process all images in the directory
    for index, filename in enumerate(image_files):
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)

        if index == 0:
            # First image uses its own orientation
            correct_image_orientation(input_path, output_path, base_rotation)
        else:
            # Rotate in the opposite direction of the last image
            if index % 2 == 1:
                rotation = (base_rotation + 180) % 360
            else:
                rotation = base_rotation

            correct_image_orientation(input_path, output_path, rotation)

        print(f"Processed: {filename}")
else:
    print("No images found in the input directory.")
