
import cv2
import numpy as np
from PIL import Image

# Ladataan kuva
image_path = 'output/corrected_img10052024_0003.tif'
image = cv2.imread(image_path)

# Muutetaan kuva harmaasävyksi
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Käytetään adaptivista kynnysarvoa saadaksemme tekstit erottumaan
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 30)

# Löydetään kontuurit
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Maskataan kontuurit mustalla
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)

# Tallennetaan maskattu kuva
masked_image_path = 'maskaus_output/masked_image.png'
cv2.imwrite(masked_image_path, image)

# Ladataan maskattu kuva ja muutetaan se CMYK-muotoon
img = Image.open(masked_image_path).convert('CMYK')

# Tallennetaan CMYK-kuva
cmyk_image_path = 'maskaus_output/cmyk_masked_image.tif'
img.save(cmyk_image_path)


print("Kuva käsitelty ja tallennettu.")
