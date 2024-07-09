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
    final_binary_file_path = 'reconstructed_folder_data.bin' 
    out_folder_path = 'Out_Test'
    binary_to_folder(final_binary_file_path,out_folder_path)
