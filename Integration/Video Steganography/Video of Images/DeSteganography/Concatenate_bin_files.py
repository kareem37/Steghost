import os
import shutil


def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
        
def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def combine_binary_files(input_folder, output_file):
    with open(output_file, 'wb') as outfile:
        for filename in sorted(os.listdir(input_folder)):
            if filename.endswith('.bin'):
                file_path = os.path.join(input_folder, filename)
                print(f"Processing {file_path}")
                binary_data = read_binary_file(file_path)
                outfile.write(binary_data)
    print(f"Combined binary file saved to {output_file}")

def main(input_folder, output_file):
    combine_binary_files(input_folder, output_file)

# Example usage:
input_folder = r'output_frames_folder_data'
output_file = r'extracted_folder_data.bin'
main(input_folder, output_file)
delete_folder(input_folder)
