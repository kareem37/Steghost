import os
from PIL import Image

def read_images(input_folder):
    images = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            img_path = os.path.join(input_folder, filename)
            images.append(Image.open(img_path))
    return images

def save_images(images, frequencies, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    counter = 0
    for img, freq in zip(images, frequencies):
        for i in range(freq):
            output_path = os.path.join(output_folder, f'{counter:04}.png')
            img.save(output_path)
            counter += 1
            if counter > 9999:
                raise ValueError("Counter exceeded 9999. Too many images to save with 4-digit naming convention.")

def main(input_folder, frequencies, output_folder):
    images = read_images(input_folder)
    if len(images) != len(frequencies):
        raise ValueError("The length of the frequencies array must match the number of images.")
    save_images(images, frequencies, output_folder)

# Example usage:
input_folder = r'input_folder'
frequencies = [6, 6, 6, 6, 6]  # Example frequencies
output_folder = r'Frames_folder'

main(input_folder, frequencies, output_folder)
