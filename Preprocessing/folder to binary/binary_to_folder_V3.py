#When retrieving, verify each chunk’s checksum and reassemble the data:
import gzip
import pickle
import hashlib
import os

def decompress_files_data(compressed_data):
    files_data = {}
    for file_path, file_content in compressed_data.items():
        files_data[file_path] = gzip.decompress(file_content)
    return files_data

def save_files(files_data, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for file_path, file_content in files_data.items():
        full_path = os.path.join(output_folder, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'wb') as f:
            f.write(file_content)

def load_chunks_from_file(input_file):
    with open(input_file, 'rb') as f:
        wrapped_chunks = pickle.load(f)
    return wrapped_chunks

def verify_and_reassemble_chunks(wrapped_chunks):
    chunks = []
    for wrapped_chunk in wrapped_chunks:
        chunk = wrapped_chunk['data']
        checksum = wrapped_chunk['checksum']
        if hashlib.sha256(chunk).hexdigest() == checksum:
            chunks.append(chunk)
        else:
            raise ValueError("Data corruption detected!")
    return b''.join(chunks)

def binary_to_folder_from_chunks(binary_file_path, output_folder):
    wrapped_chunks = load_chunks_from_file(binary_file_path)
    binary_data = verify_and_reassemble_chunks(wrapped_chunks)
    compressed_data = pickle.loads(binary_data)
    files_data = decompress_files_data(compressed_data)
    save_files(files_data, output_folder)

# Example usage
if __name__ == "__main__":
    binary_to_folder_from_chunks(r'C:\Users\Kareem Ashraf\OneDrive\Desktop\output_chunks.bin', r'C:\Users\Kareem Ashraf\OneDrive\Desktop\reconstructed_folder')
