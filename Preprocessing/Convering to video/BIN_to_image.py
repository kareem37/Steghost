import numpy as np
import cv2
import os

def binary_to_images(binary_file_path, output_dir, image_size=(1024, 1024)):
    with open(binary_file_path, 'rb') as f:
        data = f.read()

    total_bytes = len(data)
    bytes_per_image = image_size[0] * image_size[1]

    os.makedirs(output_dir, exist_ok=True)

    index = 0
    for i in range(0, total_bytes, bytes_per_image):
        chunk = data[i:i+bytes_per_image]
        if len(chunk) < bytes_per_image:
            chunk += bytes([0] * (bytes_per_image - len(chunk)))

        image = np.frombuffer(chunk, dtype=np.uint8).reshape(image_size)
        image_path = os.path.join(output_dir, f'image_{index:04d}.png')
        cv2.imwrite(image_path, image)
        index += 1

    print(f"{index} images created in '{output_dir}'")

# Example usage
binary_file_path = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output_binary_file.bin'
output_dir = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output images'

binary_to_images(binary_file_path, output_dir)
