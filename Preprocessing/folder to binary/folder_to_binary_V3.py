#  split the BIN file into smaller chunks and add metadata to each chunk. 
# This metadata can include the order of the chunks, checksums, and error correction codes.

# (Using gzip) 601 MB --> 34.326 seconds + 11.336 seconds (BIN Size = 648 MB)

import gzip
import pickle
import hashlib
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


def compress_files_data(files_data):
    compressed_data = {}
    for file_path, file_content in files_data.items():
        compressed_data[file_path] = gzip.compress(file_content)
    return compressed_data

def chunk_data(data, chunk_size):
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

def add_metadata(chunks):
    wrapped_chunks = []
    for index, chunk in enumerate(chunks):
        checksum = hashlib.sha256(chunk).hexdigest()
        wrapped_chunks.append({
            'index': index,
            'data': chunk,
            'checksum': checksum
        })
    return wrapped_chunks

def save_chunks_to_file(wrapped_chunks, output_file):
    with open(output_file, 'wb') as f:
        pickle.dump(wrapped_chunks, f)

def folder_to_binary_with_chunks(folder_path, binary_file_path, chunk_size=1024):
    files_data = read_files_in_folder(folder_path)
    compressed_data = compress_files_data(files_data)
    binary_data = pickle.dumps(compressed_data)
    chunks = chunk_data(binary_data, chunk_size)
    wrapped_chunks = add_metadata(chunks)
    save_chunks_to_file(wrapped_chunks, binary_file_path)

# Example usage
if __name__ == "__main__":
    folder_to_binary_with_chunks(r'C:\Users\Kareem Ashraf\OneDrive\Desktop\test', r'C:\Users\Kareem Ashraf\OneDrive\Desktop\output_chunks.bin')
