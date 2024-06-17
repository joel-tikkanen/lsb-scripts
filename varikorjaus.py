import cv2
import numpy as np
from PIL import Image
import os

LIGHEST_POINT = [240, 215, 179]
DARKEST_POINT = [1, 0, 0]

def correct_colors(
    image_path, output_path, new_white_point=(254, 254, 254), margin=250
):
    # Lataa kuvan
    image = Image.open(image_path)
    image = np.array(image)

    # Käytetään vain RGB-kanavia, jos kuvassa on neljä kanavaa
    if image.shape[-1] == 4:
        image = image[:, :, :3]

    # Jos kuva on harmaasävyinen tai yksikanavainen, muutetaan se RGB-muotoon
    if len(image.shape) == 2 or image.shape[-1] == 1:  # Harmaasävystä RGB:ksi
        image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image_rgb = image

    # Kuvan dimensiot
    height, width, _ = image_rgb.shape

    # Etsitään tummin piste marginaalien sisältä, täysin tummia pisteitä huomioimatta.
    reshaped_image = image_rgb[
        margin : height - margin, margin : width - margin
    ].reshape((-1, 3))
    valid_dark_pixels = reshaped_image[np.all(reshaped_image > DARKEST_POINT, axis=1)]
    if valid_dark_pixels.size == 0:
        raise ValueError("No valid dark pixels found that are not absolute black.")
    darkest_point = np.min(valid_dark_pixels, axis=0).astype(np.float32)

    # Etsitään vaalein piste marginaalien sisältä, täysin valkoisia pisteitä huomioimatta.
    margin_pixels = image_rgb[
        margin : height - margin, margin : width - margin
    ].reshape(-1, 3)
    valid_pixels = margin_pixels[np.all(margin_pixels < LIGHEST_POINT, axis=1)]
    if valid_pixels.size == 0:
        raise ValueError("No valid pixels found that are not near-white.")
    lightest_point = np.max(valid_pixels, axis=0).astype(np.float32)

    # Tulostetaan tummin ja vaalein väri.
    print(f"Darkest point: {darkest_point}")
    print(f"Lightest point: {lightest_point}")

    # Normalisoidaan värit välille [0, 1]
    normalized = (image_rgb.astype(np.float32) - darkest_point) / (
        lightest_point - darkest_point
    )
    normalized = np.clip(normalized, 0, 1)

    # Skaalataan värit uudelle valkoiselle pisteelle
    new_white_point_array = np.array(new_white_point, dtype=np.float32)
    corrected = normalized * new_white_point_array
    corrected = np.clip(corrected, 0, 255).astype(np.uint8)

    # Tallennetaan kuva
    adjusted_image_pil = Image.fromarray(corrected)
    adjusted_image_pil.save(output_path)
    return output_path


def process_images(input_folder, output_folder):
    # Varmistetaan, että output-kansio on olemassa
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Käydään läpi kaikki kuvat input-kansiossa
    for filename in os.listdir(input_folder):
        if filename.endswith((".tif", ".jpg", ".png", ".jpeg")):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, "corrected_" + filename)
            try:
                corrected_image_path = correct_colors(
                    input_image_path, output_image_path
                )
                print(f"Corrected image saved at {corrected_image_path}")
            except Exception as e:
                print(f"Error processing {input_image_path}: {e}")


# Määritetään input- ja output-kansioiden polut
input_folder = "/Users/joeltikkanen/Documents/lsb/kaanto_output"
output_folder = "/Users/joeltikkanen/Documents/lsb/output"
process_images(input_folder, output_folder)
