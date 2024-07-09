# THe improvement here is in the size of the BIN file 
# (Using gzip) 83 MB --> 2.968 seconds + 0.547 seconds (BIN Size = 82 MB) 
# (Using gzip) 1.28 GB --> 63.979 seconds + 11.835 seconds (BIN Size = 1.28 GB)
# ===================================================================
# (Using lzma) 29 MB --> 8.389 seconds + 1.219 seconds (BIN Size = 26.5 MB)
# (Using lzma) 601 MB --> 457.803 seconds + 14.17 seconds (BIN Size = 595 MB)
# ===================================================================
# (Using zstd) 601 MB --> 3.796 seconds + 2.625 seconds (BIN Size = 595 MB)
# (Using zstd) 29 MB --> 0.343 seconds + 0.259 seconds (BIN Size = 26 MB)


import os
import pickle
import lzma
import gzip
import zstandard as zstd
#import pyzipper



def read_files_in_folder(folder_path):
    files_data = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                relative_path = os.path.relpath(file_path, folder_path)
                files_data[relative_path] = f.read()
    return files_data

# GZIP
# def compress_files_data(files_data):
#     compressed_data = {}
#     for file_path, file_content in files_data.items():
#         compressed_data[file_path] = gzip.compress(file_content)
#     return compressed_data

# LZMA
# def compress_files_data(files_data):
#     compressed_data = {}
#     for file_path, file_content in files_data.items():
#         compressed_data[file_path] = lzma.compress(file_content)
#     return compressed_data

#ZSTD
def compress_files_data(files_data):
    compressed_data = {}
    compressor = zstd.ZstdCompressor()
    for file_path, file_content in files_data.items():
        compressed_data[file_path] = compressor.compress(file_content)
    return compressed_data

def save_compressed_data(compressed_data, output_file):
    with open(output_file, 'wb') as f:
        pickle.dump(compressed_data, f)

def folder_to_binary(folder_path, binary_file_path):
    files_data = read_files_in_folder(folder_path)
    compressed_data = compress_files_data(files_data)
    save_compressed_data(compressed_data, binary_file_path)

# Example usage
if __name__ == "__main__":
    folder_path = r'test'
    folder_to_binary(folder_path, 'folder_data.bin')
