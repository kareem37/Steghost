import subprocess
import os

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

# Example usage
key = 23
data_bit_count = 24
filename = r'E:\(4)\GP2024\Final\Steghost\Data Distributing\Frames_folder_data\chunk_0000.bin'
in_image_path = r'E:\(4)\GP2024\Final\Steghost\Data Distributing\Frames_folder_images\0000.png'
out_image_path = r'E:\(4)\GP2024\Final\Steghost\Data Distributing\input_frames_video\0000.png'
Stego_Time_file = r"E:\(4)\GP2024\Final\Steghost\Data Distributing\TimeComplexity\steganography_time_complexity.txt"
script_path = r"E:\(4)\GP2024\Final\Steghost\Puzzle_LSB\F5 _v8\F5_Steganography.py"  # The relative path to the F5_Steganography.py script

run_f5_steganography(script_path, key, data_bit_count, filename, in_image_path, out_image_path, Stego_Time_file)
