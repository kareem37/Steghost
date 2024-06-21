import cv2
import os

def images_to_video(images_dir, output_video_path, fps=30, image_size=(1024, 1024)):
    # Get sorted list of image files
    image_files = sorted([f for f in os.listdir(images_dir) if f.endswith('.png')])
    if not image_files:
        print("No images found in the directory.")
        return

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, image_size)

    for image_file in image_files:
        image_path = os.path.join(images_dir, image_file)
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, image_size)
        video_writer.write(resized_image)

    video_writer.release()
    print(f"Video saved to '{output_video_path}'")

# Example usage
images_dir = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output images'
output_video_path = r'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output_video.mp4'

images_to_video(images_dir, output_video_path)
