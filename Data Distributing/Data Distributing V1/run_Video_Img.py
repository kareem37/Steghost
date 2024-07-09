import subprocess

def run_video_to_images(script_path, video_path, output_folder):
    subprocess.run([
        "python", script_path,
        "--video_path", video_path,
        "--output_folder", output_folder,
    ])

script_path = r"E:\(4)\GP2024\Final\Steghost\Video Image Converter\Video Image Converter V2\Video_Img.py"  # Replace with the path to the video_to_images.py script
video_path = r"E:\(4)\GP2024\Final\Steghost\Data Distributing\Data Distributing V1\Steghost_video.avi"  # Path to the video created in Step 1
output_folder = r"E:\(4)\GP2024\Final\Steghost\Data Distributing\Data Distributing V1\output_frames_video"  # Folder to save extracted images


run_video_to_images( script_path, video_path, output_folder)