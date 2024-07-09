import subprocess
import os
import shutil

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
def run_f5_steganography(script_path, key, data_bit_count, filename, in_image_path, out_image_path, Stego_Time_file):
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

# Example usage
key = 23
data_bit_count = 24
base_folder = r'E:\(4)\GP2024\Final\Steghost\Data Distributing\Data Distributing V1'
frames_folder_data = os.path.join(base_folder, 'input_frames_folder_data')
frames_folder_images = os.path.join(base_folder, 'Frames_folder_images')
input_frames_video = os.path.join(base_folder, 'input_frames_video')
time_complexity_folder = os.path.join(base_folder, 'TimeComplexity')
script_path = r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v8\F5_Steganography.py"  # The path to the F5_Steganography.py script

clear_output_folder(input_frames_video)
loop_count = get_loop_count(frames_folder_data)

for i in range(loop_count):
    file_index = f'{i:04d}'
    filename = os.path.join(frames_folder_data, f'chunk_{file_index}.bin')
    in_image_path = os.path.join(frames_folder_images, f'{file_index}.png')
    out_image_path = os.path.join(input_frames_video, f'{file_index}.png')
    Stego_Time_file = os.path.join(time_complexity_folder, f'{file_index}.txt')

    run_f5_steganography(script_path, key, data_bit_count, filename, in_image_path, out_image_path, Stego_Time_file)
