import subprocess
import os
import shutil


def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
        
def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    

def run_DeSteganography(script_path, key, data_bit_count, in_image_path, out_filename, DeStego_Time_file):
    subprocess.run([
        "python", script_path,
        "--key", str(key),
        "--data_bit_count", str(data_bit_count),
        "--in_image_path", in_image_path,
        "--out_filename", out_filename,
        "--DeStego_Time_file", DeStego_Time_file
    ])

def get_loop_count(folder_path):
    return len([name for name in os.listdir(folder_path) if name.endswith('.png')])

# Example usage
key = 23
data_bit_count = 24
base_folder = r'E:\(4)\GP2024\Final\Steghost\Integration\Video Steganography\Part of Video\DeSteganography'
output_frames_folder_data = os.path.join(base_folder, 'output_frames_folder_data')
Extracted_Video_Frames = os.path.join(base_folder, 'Extracted_Video_Frames')
time_complexity_folder = os.path.join(base_folder, 'User_Output_Statistics\DeSteganographyTimeComplexity')

clear_output_folder(output_frames_folder_data)
clear_output_folder(time_complexity_folder)

loop_count = get_loop_count(Extracted_Video_Frames)

# Paths to the different steganography scripts
script_paths = {
    "LSB_4": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_DeSteganography.py",
    "F5": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_DeSteganography.py",
    "Adaptive_threshold": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_DeSteganography.py"
}

# Pattern for applying algorithms
algorithm_pattern = ["LSB_4", "LSB_4", "LSB_4", "F5", "F5", "Adaptive_threshold"]

for i in range(loop_count):
    file_index = f'{i:05d}'
    out_filename = os.path.join(output_frames_folder_data, f'chunk_{file_index}.bin')
    in_image_path = os.path.join(Extracted_Video_Frames, f'frame{file_index}.png')
    DeStego_Time_file = os.path.join(time_complexity_folder, f'{file_index}.txt')
    # Determine which algorithm to use based on the pattern
    algorithm = algorithm_pattern[i % len(algorithm_pattern)]
    script_path = script_paths[algorithm]

    run_DeSteganography(script_path, key, data_bit_count, in_image_path, out_filename, DeStego_Time_file)
    
delete_folder(Extracted_Video_Frames)
