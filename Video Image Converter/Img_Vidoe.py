import cv2
import os

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

input_folder = r"Out_Folder"  # Replace with your folder path
output_video = r"output_video.avi"  # Replace with desired output video path (using .avi)

images_to_video(input_folder, output_video)
