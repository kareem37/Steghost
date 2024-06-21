import cv2
import os

def video_to_images(video_path, output_dir, image_size=(1024, 1024)):
    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print("Error opening video file.")
        return

    os.makedirs(output_dir, exist_ok=True)

    frame_index = 0
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, image_size)
        image_path = os.path.join(output_dir, f'image_{frame_index:04d}.png')
        cv2.imwrite(image_path, resized_frame)
        frame_index += 1

    video_capture.release()
    print(f"{frame_index} images saved to '{output_dir}'")

# Example usage
video_path = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\prettty_720.mp4'
output_images_dir = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\extracted_images'

video_to_images(video_path, output_images_dir)
