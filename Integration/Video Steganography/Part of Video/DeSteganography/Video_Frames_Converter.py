import os
import shutil
import cv2

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

def main():
    video_path = r"User_Input\Steganography_Video.avi"
    output_folder = "Extracted_Video_Frames"
    video_to_images(video_path, output_folder)
    print(f"Extracted frames are saved in {output_folder}")

if __name__ == "__main__":
    main()
