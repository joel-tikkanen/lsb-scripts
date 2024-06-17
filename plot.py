import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Paths to the images
before_path = '/Users/joeltikkanen/Documents/lsb/kaanto_output/img10052024_0091.tif'
after_path = '/Users/joeltikkanen/Documents/lsb/output/corrected_img10052024_0091.tif'

# Load the images
img_before = mpimg.imread(before_path)
img_after = mpimg.imread(after_path)

# Plot the images side by side
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Plot the image before color correction
axes[0].imshow(img_before)
axes[0].set_title('Before Color Correction')
axes[0].axis('off')  # Hide axis

# Plot the image after color correction
axes[1].imshow(img_after)
axes[1].set_title('After Color Correction')
axes[1].axis('off')  # Hide axis

# Display the plot
plt.tight_layout()
plt.show()
