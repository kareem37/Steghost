import subprocess
import os

def convert_avi_to_mp4(input_avi, output_mp4):
    command = [
        'ffmpeg', '-i', input_avi, '-c:v', 'libx264', 
        '-preset', 'veryslow', '-qp', '0', output_mp4
    ]
    subprocess.run(command, check=True)

def convert_mp4_to_avi(input_mp4, output_avi):
    command = [
        'ffmpeg', '-i', input_mp4, '-c:v', 'ffv1', output_avi
    ]
    subprocess.run(command, check=True)

# Example usage
input_avi = 'output_video.avi'
output_mp4 = 'converted_output.mp4'
output_back_to_avi = 'converted_back_output.avi'

# Convert AVI to MP4
convert_avi_to_mp4(input_avi, output_mp4)

# Convert MP4 back to AVI
convert_mp4_to_avi(output_mp4, output_back_to_avi)
