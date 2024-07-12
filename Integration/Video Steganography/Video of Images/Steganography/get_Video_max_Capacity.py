import cv2
import os
from PIL import Image

def get_frame_dimensions(input_folder):
    image_path = os.path.join(input_folder, "00000.png")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"{image_path} does not exist in the specified folder.")
    
    with Image.open(image_path) as img:
        width, height = img.size
    
    return width, height

def write_dimensions_to_file(output_file, total_capacity):
    # Calculate capacity in different units
    capacity_in_bytes = total_capacity / 8
    capacity_in_kilobytes = capacity_in_bytes / 1024
    capacity_in_megabytes = capacity_in_kilobytes / 1024
    capacity_in_gigabytes = capacity_in_megabytes / 1024

    # Write the capacities to the file
    with open(output_file, 'w') as file:
        file.write(f"Total Capacity: {total_capacity} bits\n")
        file.write(f"Total Capacity: {capacity_in_bytes:.2f} bytes\n")
        file.write(f"Total Capacity: {capacity_in_kilobytes:.2f} KB\n")
        file.write(f"Total Capacity: {capacity_in_megabytes:.2f} MB\n")
        file.write(f"Total Capacity: {capacity_in_gigabytes:.2f} GB\n")
        file.write(f"==============================================\n")
        
def write_Algorithms_Capacity_to_file(output_file2, width, height):
    # Calculate capacity in different units
    LSB_4_capacity_in_bits = (width * height * 3 - 24) #TODO: width * height * 3 * 4 
    F5_capacity_in_bits = (width * height * 3 - 24) 
    Adaptive_threshold_capacity_in_bits = int (width * height * 2.5)
    
    # Write the capacities to the file
    with open(output_file2, 'w') as file:
        file.write(f"LSB_4 Capacity: {LSB_4_capacity_in_bits} bits Per Frame\n")
        file.write(f"F5 Capacity: {F5_capacity_in_bits} bits Per Frame\n")
        file.write(f"Adaptive_threshold Capacity: {Adaptive_threshold_capacity_in_bits} bits Per Frame\n")
        file.write(f"==============================================\n")


def LSB_4_get_max_capacity_data_to_store(width, height, FramesCount):
    return width * height * 3 * 4 * FramesCount

def F5_get_max_capacity_data_to_store(width, height, FramesCount):
    F5_data_bit_count = 24 # in bits
    return (width * height * 3 - F5_data_bit_count) * FramesCount

def Adaptive_threshold_get_max_capacity_data_to_store(width, height, FramesCount):
    return int(width * height * 2.5 * FramesCount)

def get_total_frames(input_folder):
    # Get a list of files in the input folder
    files = os.listdir(input_folder)
    
    # Filter the list to include only .png files
    images = [f for f in files if f.endswith('.png')]
    
    if not images:
        raise FileNotFoundError("No .png images found in the specified folder.")
    
    # Return the number of .png images
    return len(images)

def calculate_total_capacity(width, height, total_frames):
    total_capacity = 0
    unit_frame = total_frames // 6
    LSB_4_frames = unit_frame * 3
    F5_frames = unit_frame * 2
    Adaptive_threshold_frames = unit_frame * 1
    reminder = total_frames % 6
    if reminder <= 3:
        LSB_4_frames += reminder
    elif reminder <= 5:
        LSB_4_frames += 3
        F5_frames += (reminder - 3)
    #print('LSB_4_frames:',LSB_4_frames)
    #print('F5_frames:', F5_frames)
    #print('Adaptive_threshold_frames:', Adaptive_threshold_frames)

    total_capacity += LSB_4_get_max_capacity_data_to_store(width, height, LSB_4_frames)
    total_capacity += F5_get_max_capacity_data_to_store(width, height, F5_frames)
    total_capacity += Adaptive_threshold_get_max_capacity_data_to_store(width, height, Adaptive_threshold_frames)

    return total_capacity

def main(Resized_Frames_folder_path, output_file1, output_file2):
    width, height = get_frame_dimensions(Resized_Frames_folder_path)
    #print(f"Dimensions of the first frame: {width}x{height}")
    write_Algorithms_Capacity_to_file(output_file2, width, height)
    total_frames = get_total_frames(Resized_Frames_folder_path)
    #print(f"Total frames of the first frame: {total_frames} frames")
    total_capacity = calculate_total_capacity(width, height, total_frames)
    write_dimensions_to_file(output_file1, total_capacity)

if __name__ == "__main__":
    Resized_Frames_folder_path = r'Resized_Frames_folder'
    output_file1 = r'User_Output_Statistics\Video_max_Capacity.txt'
    output_file2 = r'User_Output_Statistics\Algorithms_max_Capacity.txt'
    main(Resized_Frames_folder_path, output_file1, output_file2)
