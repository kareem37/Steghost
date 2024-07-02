import numpy as np
from PIL import Image

def rgb_to_gray_diff(rgb_image_path, target_gray_image_path):
    # Load the RGB image
    rgb_image = Image.open(rgb_image_path)
    
    # Convert the RGB image to grayscale
    gray_image = rgb_image.convert('L')
    
    # Load the target grayscale image
    target_gray_image = Image.open(target_gray_image_path)
    
    # Convert images to numpy arrays
    gray_image_np = np.array(gray_image)
    target_gray_image_np = np.array(target_gray_image)
    
    # Ensure the dimensions match
    if gray_image_np.shape != target_gray_image_np.shape:
        raise ValueError("The dimensions of the two images do not match.")
    
    # Calculate the number of differing pixels
    diff_pixels = np.sum(gray_image_np != target_gray_image_np)
    
    return diff_pixels

# Example usage
rgb_image_path = 'updated_rgb_image.png'
target_gray_image_path = 'reconstructed_gray_image.png'
num_diff_pixels = rgb_to_gray_diff(rgb_image_path, target_gray_image_path)
print(f"Number of differing pixels: {num_diff_pixels}")
