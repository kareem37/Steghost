import os
import cv2
import numpy as np
import shutil
from skimage.metrics import structural_similarity as ssim

def delete_folders(*folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

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

def write_results_to_file(output_path, total_diff_bits, total_bits, total_diff_percentage, avg_ssim_score):
    with open(output_path, 'w') as f:
        f.write(f"Total count of diff bits: {total_diff_bits} / {total_bits}, Percentage: {total_diff_percentage:.2f}%\n")
        f.write(f"SSIM = {avg_ssim_score:.4f}: //SSIM in (0, 1): Indicates the degree of similarity. The closer to 1, the more similar the Videos Frames are.\n")

def process_folders(Stego_Images_folder, Original_Images_folder, output_file_path):
    stego_files = sorted(os.listdir(Stego_Images_folder))
    original_files = sorted(os.listdir(Original_Images_folder))

    total_diff_bits = 0
    total_bits = 0
    total_diff_percentage = 0
    total_ssim_score = 0
    count = 0

    for stego_file in stego_files:
        stego_path = os.path.join(Stego_Images_folder, stego_file)
        original_path = os.path.join(Original_Images_folder, stego_file)

        if os.path.isfile(stego_path) and os.path.isfile(original_path):
            diff_bits, bits, diff_percentage = calculate_bit_difference(stego_path, original_path)
            ssim_score = calculate_ssim(stego_path, original_path)

            total_diff_bits += diff_bits
            total_bits += bits
            total_diff_percentage += diff_percentage
            total_ssim_score += ssim_score
            count += 1

    avg_diff_percentage = total_diff_percentage / count if count != 0 else 0
    avg_ssim_score = total_ssim_score / count if count != 0 else 0

    write_results_to_file(output_file_path, total_diff_bits, total_bits, avg_diff_percentage, avg_ssim_score)

# Paths to the folders
Stego_Images_folder = 'input_frames_to_video'
Original_Images_folder = 'Resized_Frames_folder'
output_file_path = 'User_Output_Statistics/Images_Differences.txt'

# Process folders and calculate differences and SSIM
process_folders(Stego_Images_folder, Original_Images_folder, output_file_path)

print(f"Results written to {output_file_path}")

# Delete the specified folders after processing all chunks
delete_folders(Original_Images_folder)
