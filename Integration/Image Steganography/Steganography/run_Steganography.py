import subprocess
import os
import shutil

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
def delete_bin_file(file_path):
    """
    Deletes a .bin file if it exists.

    Parameters:
    file_path (str): The path to the .bin file to be deleted.

    Returns:
    bool: True if the file was successfully deleted, False otherwise.
    """
    try:
        if os.path.isfile(file_path) and file_path.endswith('.bin'):
            os.remove(file_path)
            print(f"File {file_path} has been deleted successfully.")
            return True
        else:
            print(f"File {file_path} does not exist or is not a .bin file.")
            return False
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")
        return False
    
def run_steganography(script_path, key, data_bit_count, filename, in_image_path, out_image_path, Stego_Time_file):
    subprocess.run([
        "python", script_path,
        "--key", str(key),
        "--data_bit_count", str(data_bit_count),
        "--filename", filename,
        "--in_image_path", in_image_path,
        "--out_image_path", out_image_path,
        "--Stego_Time_file", Stego_Time_file
    ])

def read_algorithm_choice(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if "Algorithm: " in line:
                return line.split("Algorithm: ")[1].strip()
    raise ValueError("Algorithm choice not found in the file")

def read_capacity(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if "Total Capacity: " in line and "bits" in line:
                return int(line.split("Total Capacity: ")[1].strip().split()[0])
    raise ValueError("Total capacity not found in the file")

def delete_folders(*folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

# Example usage
key = 23
data_bit_count = 24
base_folder = r'E:\(4)\GP2024\Final\Steghost\Integration\Image Steganography\Steganography'
input_folder_data = base_folder
input_folder_image = os.path.join(base_folder, 'User_Cover_Image')
output_folder_image = os.path.join(base_folder, 'User_Output_Image')
time_complexity_folder = os.path.join(base_folder, 'User_Output_Statistics\Steganography_TimeComplexity')

# Paths to the different steganography scripts
script_paths = {
    "LSB4": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_Steganography.py", # Update with actual path
    "F5": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_Steganography.py", 
    "Adaptive Thresholding": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_Steganography.py" # Update with actual path
}

clear_output_folder(output_folder_image)
clear_output_folder(time_complexity_folder)

# Read the algorithm choice from Image_max_Capacity.txt
image_max_capacity_file = r'User_Output_Statistics\Image_max_Capacity.txt'
algorithm = read_algorithm_choice(image_max_capacity_file)
image_max_capacity = read_capacity(image_max_capacity_file)

# Read the data capacity from folder_data_Capacity.txt
data_capacity_file = os.path.join(base_folder, 'User_Output_Statistics\\folder_data_Capacity.txt')
data_capacity = read_capacity(data_capacity_file)

if data_capacity <= image_max_capacity:
    script_path = script_paths[algorithm]

    # File paths
    filename = os.path.join(input_folder_data, 'encrypted_data.bin')
    in_image_path = os.path.join(input_folder_image, 'image.png')
    out_image_path = os.path.join(output_folder_image, 'stego_image.png')
    Stego_Time_file = os.path.join(time_complexity_folder, 'stego_time.txt')

    # Run the steganography process
    run_steganography(script_path, key, data_bit_count, filename, in_image_path, out_image_path, Stego_Time_file)
    delete_bin_file(filename)

else:
    print("Data capacity exceeds image capacity. Steganography not performed.")


