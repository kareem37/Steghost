import os
from PIL import Image

def read_algorithm_choice(file_path):
    with open(file_path, 'r') as file:
        algorithm_choice = int(file.read().strip())
    return algorithm_choice

def get_image_dimensions(image_path):
    img = Image.open(image_path)
    width, height = img.size
    return width, height

def write_max_capacity_to_file(output_file, algorithm_choice, max_capacity):
    algorithm_name = {1: "LSB4", 2: "F5", 3: "Adaptive Thresholding"}
    with open(output_file, 'w') as file:
        file.write(f"Algorithm: {algorithm_name[algorithm_choice]}\n")
        file.write(f"Total Capacity: {max_capacity} bits\n")
        file.write(f"Total Capacity: {max_capacity / 8:.2f} bytes\n")
        file.write(f"Total Capacity: {max_capacity / 8 / 1024:.2f} KB\n")
        file.write(f"Total Capacity: {max_capacity / 8 / 1024 / 1024:.2f} MB\n")
        file.write(f"Total Capacity: {max_capacity / 8 / 1024 / 1024 / 1024:.2f} GB\n")

def LSB4_max_capacity(width, height):
    return width * height * 3 * 4

def F5_max_capacity(width, height):
    F5_data_bit_count = 24  # in bits
    return (width * height * 3 - F5_data_bit_count)

def Adaptive_threshold_max_capacity(width, height):
    return int(width * height * 2.5)

def calculate_max_capacity(width, height, algorithm_choice):
    if algorithm_choice == 1:
        return LSB4_max_capacity(width, height)
    elif algorithm_choice == 2:
        return F5_max_capacity(width, height)
    elif algorithm_choice == 3:
        return Adaptive_threshold_max_capacity(width, height)
    else:
        raise ValueError("Invalid algorithm choice")

def main(image_path, algorithm_file, output_file):
    width, height = get_image_dimensions(image_path)
    algorithm_choice = read_algorithm_choice(algorithm_file)
    max_capacity = calculate_max_capacity(width, height, algorithm_choice)
    write_max_capacity_to_file(output_file, algorithm_choice, max_capacity)

if __name__ == "__main__":
    image_path = r'User_Cover_Image\image.png'
    algorithm_file = r'User_Cover_Image\Algorithm.txt'
    output_file = r'User_Output_Statistics\Image_max_Capacity.txt'
    main(image_path, algorithm_file, output_file)
