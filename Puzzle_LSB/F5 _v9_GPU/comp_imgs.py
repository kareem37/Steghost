from PIL import Image
import numpy as np

def get_pixels_array(image_path):
    with Image.open(image_path) as image:
        image = image.convert("RGB")
        pixels = np.array(image)
    return pixels

def compare_images(image_path1, image_path2):
    # Load the images and get their pixel arrays
    pixels1 = get_pixels_array(image_path1)
    pixels2 = get_pixels_array(image_path2)
    
    # Check if the shapes of the two images are the same
    if pixels1.shape != pixels2.shape:
        return False
    
    # Compare the pixel values
    identical = np.array_equal(pixels1, pixels2)
    
    return identical

# Example usage
image_path1 = 'image.png'  
image_path2 = 'reconstructed_image.png'  

if compare_images(image_path1, image_path2):
    print("The images are identical.")
else:
    print("The images are not identical.")
