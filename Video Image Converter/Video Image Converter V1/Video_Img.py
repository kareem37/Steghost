import cv2
import os
import argparse
import shutil

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

def video_to_images(video_path, output_folder):
    clear_output_folder(output_folder)

    video = cv2.VideoCapture(video_path)
    success, image = video.read()
    count = 0

    while success:
        cv2.imwrite(os.path.join(output_folder, f"frame{count:05d}.png"), image)
        success, image = video.read()
        count += 1

    video.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract images from video")
    parser.add_argument("--video_path", type=str, required=True, help="Path to the video file")
    parser.add_argument("--output_folder", type=str, required=True, help="Folder to save extracted images")

    args = parser.parse_args()

    video_to_images(args.video_path, args.output_folder)
