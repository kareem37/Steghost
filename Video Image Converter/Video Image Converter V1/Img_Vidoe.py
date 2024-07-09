import cv2
import os
import argparse
import numpy as np

def get_max_dimensions(input_folder):
    max_height = 0
    max_width = 0
    images = [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")]
    for image in images:
        img_path = os.path.join(input_folder, image)
        img = cv2.imread(img_path)
        height, width, _ = img.shape
        if height > max_height:
            max_height = height
        if width > max_width:
            max_width = width
    return max_height, max_width

def pad_image(image, target_height, target_width):
    height, width, _ = image.shape
    top = (target_height - height) // 2
    bottom = target_height - height - top
    left = (target_width - width) // 2
    right = target_width - width - left
    color = [0, 0, 0]  # Padding color (black)

    padded_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return padded_image

def images_to_video(input_folder, output_video, fps=30):
    images = [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()

    target_height, target_width = get_max_dimensions(input_folder)

    # Use FFV1 codec for lossless compression
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    video = cv2.VideoWriter(output_video, fourcc, fps, (target_width, target_height))

    for image in images:
        img_path = os.path.join(input_folder, image)
        img = cv2.imread(img_path)
        padded_img = pad_image(img, target_height, target_width)
        video.write(padded_img)

    video.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to video")
    parser.add_argument("--input_folder", type=str, required=True, help="Path to the input folder containing images")
    parser.add_argument("--output_video", type=str, required=True, help="Path to the output video file")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for the output video")

    args = parser.parse_args()

    images_to_video(args.input_folder, args.output_video, args.fps)
