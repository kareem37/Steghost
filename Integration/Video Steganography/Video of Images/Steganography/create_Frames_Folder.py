import os
import shutil
from PIL import Image

def delete_folders(*folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            
def read_frequencies(file_path):
    # Open the file and read the lines
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Convert the lines to integers and store them in an array
    frequency_array = [int(line.strip()) for line in lines]
    
    return frequency_array

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
            output_path = os.path.join(output_folder, f'{counter:05}.png')
            img.save(output_path)
            counter += 1
            if counter > 99999:
                raise ValueError("Counter exceeded 9999. Too many images to save with 5-digit naming convention.")

def main(input_folder, frequencies, output_folder):
    images = read_images(input_folder)
    if len(images) != len(frequencies):
        raise ValueError("The length of the frequencies array must match the number of images.")
    save_images(images, frequencies, output_folder)

# Example usage:
input_folder = r'User_Cover_png_Images'
frequencies_path = r'User_Cover_Images\Images_Frequency.txt'
frequency_array = read_frequencies(frequencies_path)
output_folder = r'Frames_folder'

main(input_folder, frequency_array, output_folder)
# Delete the specified folders after processing all chunks
delete_folders(input_folder)