import subprocess
import os
import shutil

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
import subprocess

def run_F5_DeSteganography(script_path, key, data_bit_count, in_image_path, out_filename, DeStego_Time_file):
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
base_folder = r'E:\(4)\GP2024\Final\Steghost\Data Distributing\Data Distributing V1'
output_frames_folder_data = os.path.join(base_folder, 'output_frames_folder_data')
output_frames_video = os.path.join(base_folder, 'output_frames_video')
time_complexity_folder = os.path.join(base_folder, 'TimeComplexity')
script_path = r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v8\F5_DeSteganography.py"  # The path to the F5_Steganography.py script

clear_output_folder(output_frames_folder_data)
loop_count = get_loop_count(output_frames_video)

for i in range(loop_count):
    file_index = f'{i:04d}'
    out_filename = os.path.join(output_frames_folder_data, f'chunk_{file_index}.bin')
    in_image_path = os.path.join(output_frames_video, f'frame0{file_index}.png')
    DeStego_Time_file = os.path.join(time_complexity_folder, f'DeSteganography_time_complexity_{file_index}.txt')

    run_F5_DeSteganography(script_path, key, data_bit_count, in_image_path, out_filename, DeStego_Time_file)
