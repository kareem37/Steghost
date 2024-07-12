import os
import gzip
import lzma
import zstandard as zstd
#import pyzipper
import pickle

#GZIP
# def decompress_files_data(compressed_data):
#     files_data = {}
#     for file_path, file_content in compressed_data.items():
#         files_data[file_path] = gzip.decompress(file_content)
#     return files_data

#LZMA
# def decompress_files_data(compressed_data):
#     files_data = {}
#     for file_path, file_content in compressed_data.items():
#         files_data[file_path] = lzma.decompress(file_content)
#     return files_data

# ZSTD
def decompress_files_data(compressed_data):
    files_data = {}
    decompressor = zstd.ZstdDecompressor()
    for file_path, file_content in compressed_data.items():
        files_data[file_path] = decompressor.decompress(file_content)
    return files_data

def delete_bin_file(file_path):
    """
    Deletes a .bin file if it exists.

    Parameters:
    file_path (str): The path to the .bin file to be deleted.

    Returns:
    bool: True if the file was successfully deleted, False otherwise.
    """
    try:
        if os.path.isfile(file_path) and file_path.endswith('.bin'):
            os.remove(file_path)
            print(f"File {file_path} has been deleted successfully.")
            return True
        else:
            print(f"File {file_path} does not exist or is not a .bin file.")
            return False
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")
        return False
    
def save_files(files_data, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for file_path, file_content in files_data.items():
        full_path = os.path.join(output_folder, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(file_content)

def binary_to_folder(binary_file_path, output_folder):
    with open(binary_file_path, 'rb') as f:
        compressed_data = pickle.load(f)
    files_data = decompress_files_data(compressed_data)
    save_files(files_data, output_folder)

# Example usage
if __name__ == "__main__":
    final_binary_file_path = 'decrypted_folder_data.bin' 
    out_folder_path = 'User_Output'
    binary_to_folder(final_binary_file_path,out_folder_path)
    delete_bin_file(final_binary_file_path)
