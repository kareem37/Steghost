import cv2
import os

def video_to_images(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    success, image = video.read()
    count = 0

    while success:
        cv2.imwrite(os.path.join(output_folder, f"frame{count:05d}.png"), image)
        success, image = video.read()
        count += 1

    video.release()

video_path = r"converted_back_output.avi"  # Path to the video created in Step 1
output_folder = r"Extracted_Images"  # Folder to save extracted images

video_to_images(video_path, output_folder)
