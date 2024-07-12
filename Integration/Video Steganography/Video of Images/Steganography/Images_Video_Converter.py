import cv2
import os
import shutil

def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
            
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

def main():
    input_folder = "input_frames_to_video"
    output_video = r"User_Output_Video\Steganography_Video.avi"
    fps = 30
    images_to_video(input_folder, output_video, fps)
    # Delete the specified folders after processing all chunks
    delete_folder(input_folder)

if __name__ == "__main__":
    main()
