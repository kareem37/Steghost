import cv2
import os
import shutil

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

def read_frames_needed(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if "Total number of frames needed" in line:
                frames_needed = int(line.split(': ')[1])
                return frames_needed
    raise ValueError("The frames needed information is not found in the file")

def video_to_images(video_path, output_folder, frames_needed):
    clear_output_folder(output_folder)

    video = cv2.VideoCapture(video_path)
    success, image = video.read()
    count = 0

    while success and count < frames_needed:
        cv2.imwrite(os.path.join(output_folder, f"frame{count:05d}.png"), image)
        success, image = video.read()
        count += 1

    video.release()

if __name__ == "__main__":
    video_path = r'User_Cover_Video\User_input.mp4'
    output_folder = 'User_Video_Frames'
    frames_needed_file = r'User_Output_Statistics\frames_needed.txt'
    
    frames_needed = read_frames_needed(frames_needed_file)
    video_to_images(video_path, output_folder, frames_needed)
