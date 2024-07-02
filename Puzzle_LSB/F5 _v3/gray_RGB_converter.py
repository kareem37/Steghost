import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

# Function to apply 2D DCT
def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Function to apply 2D inverse DCT
def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

# Step 1: Read the images
original_rgb_image = Image.open('image.png')
target_gray_image = Image.open('reconstructed_gray_image.png')

# Convert images to numpy arrays
original_rgb_np = np.array(original_rgb_image)
target_gray_np = np.array(target_gray_image)

# Step 2: Convert the target grayscale image to its DCT coefficients
target_gray_dct = dct2(target_gray_np)

# Step 3: Convert the original RGB image to grayscale and get its DCT coefficients
original_gray_image = original_rgb_image.convert('L')
original_gray_np = np.array(original_gray_image)
original_gray_dct = dct2(original_gray_np)

# Step 4: Replace the DCT coefficients of the original grayscale image with those of the target grayscale image
updated_gray_dct = target_gray_dct

# Step 5: Apply inverse DCT to get the updated grayscale image
updated_gray_image = idct2(updated_gray_dct)
updated_gray_image = np.clip(updated_gray_image, 0, 255)
updated_gray_image = updated_gray_image.astype(np.uint8)

# Adjust the RGB channels of the original image
def adjust_rgb_channel(channel, target_gray, original_gray):
    scale = target_gray.astype(np.float32) / (original_gray.astype(np.float32) + 1e-5)
    adjusted_channel = channel.astype(np.float32) * scale
    adjusted_channel = np.clip(adjusted_channel, 0, 255)
    return adjusted_channel.astype(np.uint8)

adjusted_r = adjust_rgb_channel(original_rgb_np[:, :, 0], updated_gray_image, original_gray_np)
adjusted_g = adjust_rgb_channel(original_rgb_np[:, :, 1], updated_gray_image, original_gray_np)
adjusted_b = adjust_rgb_channel(original_rgb_np[:, :, 2], updated_gray_image, original_gray_np)

# Combine adjusted channels to form the updated RGB image
updated_rgb_image = np.stack((adjusted_r, adjusted_g, adjusted_b), axis=-1)
updated_rgb_image = Image.fromarray(updated_rgb_image)

# Save or display the updated RGB image
updated_rgb_image.show()
updated_rgb_image.save('updated_rgb_image.png')

print("Updated RGB image saved as 'updated_rgb_image.png'")
