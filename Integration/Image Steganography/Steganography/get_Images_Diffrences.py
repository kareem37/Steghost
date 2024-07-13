import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def calculate_bit_difference(image1_path, image2_path):
    # Load images
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Check if images are of the same size
    if image1.shape != image2.shape:
        raise ValueError("Images must have the same dimensions")
    
    # Calculate the bit difference
    diff = np.bitwise_xor(image1, image2)
    total_bits = image1.size * 8  # total number of bits (since each pixel is 8 bits)
    diff_bits = np.sum(np.unpackbits(diff))
    diff_percentage = (diff_bits / total_bits) * 100

    return diff_bits, total_bits, diff_percentage

def calculate_ssim(image1_path, image2_path):
    # Load images
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    # Calculate SSIM
    score, _ = ssim(image1, image2, full=True)
    
    return score

def write_results_to_file(output_path, diff_bits, total_bits, diff_percentage, ssim_score):
    with open(output_path, 'w') as f:
        f.write(f"Total count of diff bits: {diff_bits} / {total_bits}, Percentage: {diff_percentage:.2f}%\n")
        f.write(f"SSIM = {ssim_score:.4f}: //SSIM in (0, 1): Indicates the degree of similarity. The closer to 1, the more similar the images are.\n")

def delete_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted image: {image_path}")
    else:
        print(f"Image not found: {image_path}")

# Paths to the images
image1_path = 'image.png'
image2_path = 'User_Output_Image/stego_image.png'
output_file_path = 'User_Output_Statistics/Images_Differences.txt'

# Calculate differences and SSIM
diff_bits, total_bits, diff_percentage = calculate_bit_difference(image1_path, image2_path)
ssim_score = calculate_ssim(image1_path, image2_path)

# Write results to file
write_results_to_file(output_file_path, diff_bits, total_bits, diff_percentage, ssim_score)

# Delete the image
delete_image(image1_path)

print(f"Results written to {output_file_path}")
