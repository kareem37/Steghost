import os
import cv2
import numpy as np

def compare_images(image1_path, image2_path):
    # Read images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # Ensure images have the same dimensions
    if img1.shape != img2.shape:
        raise ValueError("Images must have the same dimensions to compare.")

    # Calculate the number of different pixels
    diff = cv2.absdiff(img1, img2)
    num_diff_pixels = np.count_nonzero(diff)

    return num_diff_pixels

def compare_folders(folder1, folder2):
    # Get list of image files in both folders
    images1 = sorted([f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f))])
    images2 = sorted([f for f in os.listdir(folder2) if os.path.isfile(os.path.join(folder2, f))])

    # Ensure both folders have the same number of images
    if len(images1) != len(images2):
        raise ValueError("Both folders must contain the same number of images.")

    # Compare images
    diff_results = {}
    for img1, img2 in zip(images1, images2):
        image1_path = os.path.join(folder1, img1)
        image2_path = os.path.join(folder2, img2)
        num_diff_pixels = compare_images(image1_path, image2_path)
        diff_results[img1] = num_diff_pixels

    return diff_results

# Example usage
folder1 = r'E:\(4)\GP2024\Final\Steghost\Data Distributing\Data Distributing V1\output_frames_video'
folder2 = r'E:\(4)\GP2024\Final\Steghost\Data Distributing\Data Distributing V1\input_frames_video'

diff_results = compare_folders(folder1, folder2)
for img, num_diff in diff_results.items():
    print(f"{img}: {num_diff} different pixels")
