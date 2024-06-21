import numpy as np
import cv2
import os

def images_to_binary(images_dir, output_binary_file, image_size=(1024, 1024)):
    files = sorted([f for f in os.listdir(images_dir) if f.endswith('.png')])

    binary_data = bytearray()
    for file in files:
        image_path = os.path.join(images_dir, file)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        binary_data.extend(image.flatten().tolist())

    with open(output_binary_file, 'wb') as f:
        f.write(binary_data)

    print(f"Binary file '{output_binary_file}' created from images in '{images_dir}'")

# Example usage
images_dir = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\extracted_images'
output_binary_file = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\reconstructed_binary_file.bin'

images_to_binary(images_dir, output_binary_file)
