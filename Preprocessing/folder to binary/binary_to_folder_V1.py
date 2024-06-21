import os

def binary_to_files(binary_data, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    lines = binary_data.split('\n')
    for line in lines:
        if line.strip():
            file_name_binary, file_content_binary = line.split(' ', 1)
            file_name = ''.join(chr(int(file_name_binary[i:i+8], 2)) for i in range(0, len(file_name_binary), 8))
            file_content = bytes(int(file_content_binary[i:i+8], 2) for i in range(0, len(file_content_binary), 8))
            file_path = os.path.join(output_folder, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(file_content)

def binary_to_folder(binary_file_path, output_folder):
    with open(binary_file_path, 'r') as f:
        binary_data = f.read()
    binary_to_files(binary_data, output_folder)

# Example usage
if __name__ == "__main__":
    binary_to_folder(r'C:\Users\Kareem Ashraf\OneDrive\Desktop\output_binary_file.bin', r'C:\Users\Kareem Ashraf\OneDrive\Desktop\reconstructed_folder')
