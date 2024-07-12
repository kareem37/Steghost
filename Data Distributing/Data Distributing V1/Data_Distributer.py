import os
import time
import shutil

def read_binary_file(binary_file_path):
    start_time = time.time()
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()
    end_time = time.time()
    print(f"Time to read binary file: {end_time - start_time:.4f} seconds")
    return binary_data

def read_capacities_file(capacities_file_path):
    start_time = time.time()
    with open(capacities_file_path, 'r') as file:
        capacities = [int(float(line.strip())) for line in file]
    end_time = time.time()
    print(f"Time to read capacities file: {end_time - start_time:.4f} seconds")
    return capacities

def split_binary_data(binary_data, capacities):
    start_time = time.time()
    byte_index = 0
    chunks = []
    total_capacity = sum(capacities)  # total capacity in bytes

    print('Total capacity in (Bytes) = ', total_capacity)
    print('Length of binary data in (Bytes) = ', len(binary_data))
    if total_capacity < len(binary_data):
        print("Error: The total capacity is less than the size of the binary file in bytes.")
        end_time = time.time()
        print(f"Time to process binary data: {end_time - start_time:.4f} seconds")
        return True, chunks
    counter = 0
    for capacity in capacities:
        chunk = binary_data[byte_index:byte_index + capacity]     
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
            counter += 1
            print(f"Chunk {counter} saved successfully.")
        byte_index += capacity

    end_time = time.time()
    print(f"Time to process binary data: {end_time - start_time:.4f} seconds")
    return False, chunks

def clear_output_folder(output_folder):
    if os.path.exists(output_folder):
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

def save_chunks_to_files(chunks, output_folder):
    start_time = time.time()
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        clear_output_folder(output_folder)

    for i, chunk in enumerate(chunks):
        if chunk:  # Save only non-empty chunks
            output_path = os.path.join(output_folder, f'chunk_{i:04d}.bin')
            with open(output_path, 'wb') as file:
                file.write(chunk)

    end_time = time.time()
    print(f"Time to save chunks to files: {end_time - start_time:.4f} seconds")

def main(binary_file_path, capacities_file_path, output_folder):
    binary_data = read_binary_file(binary_file_path)
    
    capacities = read_capacities_file(capacities_file_path)

    error, chunks = split_binary_data(binary_data, capacities)
    if not error:
        save_chunks_to_files(chunks, output_folder)
        print(f"Chunks have been saved to {output_folder}")
    else:
        print("Insufficient capacity to store the binary file.")

# Example usage:
binary_file_path = r'folder_data.bin'
capacities_file_path = r'Capacities_file.txt'
output_folder = r'input_frames_folder_data'

main(binary_file_path, capacities_file_path, output_folder)
