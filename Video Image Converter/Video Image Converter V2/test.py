import subprocess

def run_images_to_video(script_path, input_folder, output_video, fps):
    subprocess.run([
        "python", script_path,
        "--input_folder", input_folder,
        "--output_video", output_video,
        "--fps", str(fps)
    ])

# Example usage

script_path = r"E:\(4)\GP2024\Final\Steghost\Video Image Converter\Video Image Converter V1\Img_Vidoe.py"  # Replace with the path to the images_to_video.py script
input_folder = r"E:\(4)\GP2024\Final\Steghost\Video Image Converter\Video Image Converter V1\Out_Folder"  # Replace with your folder path
output_video = r"E:\(4)\GP2024\Final\Steghost\Video Image Converter\Video Image Converter V1\Steghost_video.avi"  # Replace with desired output video path (using .avi)
fps = 6

run_images_to_video(script_path, input_folder, output_video, fps)
# ###----------------------------------------------------------------


