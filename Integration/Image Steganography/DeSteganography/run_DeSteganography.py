import subprocess
import os
import shutil



def run_DeSteganography(script_path, key, data_bit_count, in_image_path, out_filename, DeStego_Time_file):
    subprocess.run([
        "python", script_path,
        "--key", str(key),
        "--data_bit_count", str(data_bit_count),
        "--in_image_path", in_image_path,
        "--out_filename", out_filename,
        "--DeStego_Time_file", DeStego_Time_file
    ])

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
    

def read_algorithm_choice(file_path):
    with open(file_path, 'r') as file:
        algorithm_choice = int(file.read().strip())
    return algorithm_choice


# Example usage
key = 23
data_bit_count = 24
base_folder = r'E:\(4)\GP2024\Final\Steghost\Integration\Image Steganography\DeSteganography'
output_data_path = base_folder
input_folder_image = os.path.join(base_folder, 'User_Input')
time_complexity_folder = os.path.join(base_folder, 'User_Output_Statistics\DeSteganographyTimeComplexity')

# Paths to the different steganography scripts
script_paths = [
    r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_DeSteganography.py",
    r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_DeSteganography.py",
    r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_DeSteganography.py"
]
# Read the algorithm choice from Image_max_Capacity.txt
algorithm_file = r'User_Input\Algorithm.txt'
algorithm = read_algorithm_choice(algorithm_file)

script_path = script_paths[algorithm - 1]
out_filename = os.path.join(output_data_path, f'extracted_folder_data.bin')
in_image_path = os.path.join(input_folder_image, f'stego_image.png')
DeStego_Time_file = os.path.join(time_complexity_folder, f'DeStego_Time.txt')
# File paths
run_DeSteganography(script_path, key, data_bit_count, in_image_path, out_filename, DeStego_Time_file)




