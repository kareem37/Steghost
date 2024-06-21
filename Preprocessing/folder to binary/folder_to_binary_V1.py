import os

def read_files_in_folder(folder_path):
    files_data = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                relative_path = os.path.relpath(file_path, folder_path)
                files_data[relative_path] = f.read()
    return files_data

def files_to_binary(files_data):
    binary_data = ''
    for file_path, file_content in files_data.items():
        file_name_binary = ''.join(format(ord(char), '08b') for char in file_path)
        file_content_binary = ''.join(format(byte, '08b') for byte in file_content)
        binary_data += file_name_binary + ' ' + file_content_binary + '\n'
    return binary_data

def save_binary_data(binary_data, output_file):
    with open(output_file, 'w') as f:
        f.write(binary_data)

def folder_to_binary(folder_path, binary_file_path):
    files_data = read_files_in_folder(folder_path)
    binary_data = files_to_binary(files_data)
    save_binary_data(binary_data, binary_file_path)

# Example usage
if __name__ == "__main__":
    folder_to_binary(r'C:\Users\Kareem Ashraf\OneDrive\Desktop\test', r'C:\Users\Kareem Ashraf\OneDrive\Desktop\output_binary_file.bin')
