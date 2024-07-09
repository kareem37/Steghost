import os
from PIL import Image

def LSB_4_get_max_capacity_data_to_store(width, height):
    return width * height * 3 * 4

def F5_get_max_capacity_data_to_store(width, height):
    F5_data_bit_count = 24 # in bits
    return width * height * 3 - F5_data_bit_count

def Adaptive_threshold_get_max_capacity_data_to_store(width, height):
    return width * height * 2.5

def ensure_rgb_image(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image

def read_images_and_calculate_capacity(input_folder):
    max_capacity = []
    img_list = [f for f in os.listdir(input_folder) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    for i, filename in enumerate(img_list):
        img_path = os.path.join(input_folder, filename)
        with Image.open(img_path) as img:
            img = ensure_rgb_image(img)
            width, height = img.size
            if i % 6 < 3:  # First 3 images for LSB_4
                capacity_bits = F5_get_max_capacity_data_to_store(width, height)
            elif i % 6 < 5:  # Next 2 images for F5
                capacity_bits = F5_get_max_capacity_data_to_store(width, height)
            else:  # Last image for Adaptive_threshold
                capacity_bits = F5_get_max_capacity_data_to_store(width, height)
            # Floor capacity to the nearest byte and convert to bytes
            capacity_bytes = capacity_bits // 8
            max_capacity.append(capacity_bytes)
    return max_capacity

def save_max_capacity_to_file(max_capacity_array, output_file):
    with open(output_file, 'w') as file:
        total_capacity = 0
        for capacity in max_capacity_array:
            total_capacity += capacity
            file.write(f"{capacity}\n")
        print("Total capacity saved to file (in bytes):", total_capacity)

def main(input_folder, output_file):
    max_capacity_array = read_images_and_calculate_capacity(input_folder)
    save_max_capacity_to_file(max_capacity_array, output_file)

# Example usage:
input_folder = r'Frames_folder_images'
output_file = r'Capacities_file.txt'
main(input_folder, output_file)

print(f"Max capacity array has been saved to {output_file}")
