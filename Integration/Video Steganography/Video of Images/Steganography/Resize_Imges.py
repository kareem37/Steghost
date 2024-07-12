import cv2
import os
import shutil

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
def delete_folders(*folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def get_min_dimensions(input_folder):
    min_height = float('inf')
    min_width = float('inf')
    images = [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")]
    for image in images:
        img_path = os.path.join(input_folder, image)
        img = cv2.imread(img_path)
        height, width, _ = img.shape
        if height < min_height:
            min_height = height
        if width < min_width:
            min_width = width
    return min_height, min_width

def resize_image(image, target_height, target_width):
    resized_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_AREA)
    return resized_image

def resize_and_save_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    clear_output_folder(output_folder)

    target_height, target_width = get_min_dimensions(input_folder)

    images = [img for img in os.listdir(input_folder) if img.endswith(".png") or img.endswith(".jpg")]

    for image in images:
        img_path = os.path.join(input_folder, image)
        img = cv2.imread(img_path)
        resized_img = resize_image(img, target_height, target_width)
        output_path = os.path.join(output_folder, image)
        cv2.imwrite(output_path, resized_img)

# Update the following variables with appropriate paths
input_folder = "Frames_folder"
output_folder = "Resized_Frames_folder"

resize_and_save_images(input_folder, output_folder)
delete_folders(input_folder)
