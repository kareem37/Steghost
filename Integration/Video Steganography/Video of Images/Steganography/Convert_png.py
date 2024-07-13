import os
from PIL import Image

def convert_images_to_png(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        # Get the file path
        file_path = os.path.join(input_folder, filename)
        
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
            # Open the image
            with Image.open(file_path) as img:
                # Convert the image to RGB (this step ensures compatibility with all formats)
                img = img.convert('RGB')
                # Define the new file path with .png extension
                new_file_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')
                # Save the image as PNG
                img.save(new_file_path, 'PNG')

            print(f'Converted {filename} to PNG and saved as {new_file_path}')

if __name__ == "__main__":
    input_folder = 'User_Cover_Images'
    output_folder = 'User_Cover_png_Images'
    convert_images_to_png(input_folder, output_folder)
