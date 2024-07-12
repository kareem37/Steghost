import subprocess
import os
import shutil

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
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

def get_loop_count(folder_path):
    return len([name for name in os.listdir(folder_path) if name.endswith('.bin')])

def delete_folders(*folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

# Example usage
key = 23
data_bit_count = 24
base_folder = r'E:\(4)\GP2024\Final\Steghost\Integration\Video Steganography\Part of Video\Steganography'
frames_folder_data = os.path.join(base_folder, 'input_frames_folder_data')
frames_folder_images = os.path.join(base_folder, 'User_Video_Frames')
input_frames_video = os.path.join(base_folder, 'input_frames_to_video')
time_complexity_folder = os.path.join(base_folder, 'User_Output_Statistics\Steganography_TimeComplexity')

# Paths to the different steganography scripts
script_paths = {
    "LSB_4": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_Steganography.py", #TODO:
    "F5": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_Steganography.py", 
    "Adaptive_threshold": r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v9_GPU\F5_Steganography.py"#TODO:
}

clear_output_folder(input_frames_video)
clear_output_folder(time_complexity_folder)
loop_count = get_loop_count(frames_folder_data)

# Pattern for applying algorithms
algorithm_pattern = ["LSB_4", "LSB_4", "LSB_4", "F5", "F5", "Adaptive_threshold"]

for i in range(loop_count):
    file_index = f'{i:05d}'
    filename = os.path.join(frames_folder_data, f'chunk_{file_index}.bin')
    in_image_path = os.path.join(frames_folder_images, f'frame{file_index}.png')
    out_image_path = os.path.join(input_frames_video, f'{file_index}.png')
    Stego_Time_file = os.path.join(time_complexity_folder, f'{file_index}.txt')
    
    # Determine which algorithm to use based on the pattern
    algorithm = algorithm_pattern[i % len(algorithm_pattern)]
    script_path = script_paths[algorithm]

    run_steganography(script_path, key, data_bit_count, filename, in_image_path, out_image_path, Stego_Time_file)

# Delete the specified folders after processing all chunks
delete_folders(frames_folder_images, frames_folder_data)
