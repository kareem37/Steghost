import cv2
import os
import argparse

def images_to_video(input_folder, output_video, fps=30):
    images = [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()

    frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = frame.shape

    # Use FFV1 codec for lossless compression
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for image in images:
        img_path = os.path.join(input_folder, image)
        video.write(cv2.imread(img_path))

    video.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert images to video")
    parser.add_argument("--input_folder", type=str, required=True, help="Path to the input folder containing images")
    parser.add_argument("--output_video", type=str, required=True, help="Path to the output video file")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for the output video")

    args = parser.parse_args()

    images_to_video(args.input_folder, args.output_video, args.fps)