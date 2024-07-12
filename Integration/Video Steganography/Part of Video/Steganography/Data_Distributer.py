import os
import time
import shutil

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
    
def read_binary_file(binary_file_path):
    start_time = time.time()
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()
    end_time = time.time()
    print(f"Time to read binary file: {end_time - start_time:.4f} seconds")
    return binary_data

def read_capacities_file(capacities_file_path):
    start_time = time.time()
    capacities = {}
    with open(capacities_file_path, 'r') as file:
        for line in file:
            if "LSB_4 Capacity" in line:
                capacities["LSB_4"] = int(line.split(': ')[1].split()[0]) // 8  # Convert bits to bytes
            elif "F5 Capacity" in line:
                capacities["F5"] = int(line.split(': ')[1].split()[0]) // 8  # Convert bits to bytes
            elif "Adaptive_threshold Capacity" in line:
                capacities["Adaptive_threshold"] = int(line.split(': ')[1].split()[0]) // 8  # Convert bits to bytes
    end_time = time.time()
    print(f"Time to read capacities file: {end_time - start_time:.4f} seconds")
    return capacities

def read_frames_needed(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if "Total number of frames needed" in line:
                frames_needed = int(line.split(': ')[1])
                return frames_needed
    raise ValueError("The frames needed information is not found in the file")

def split_binary_data(binary_data, capacities, frames_needed):
    start_time = time.time()
    byte_index = 0
    chunks = []
    frame_pattern = ["LSB_4", "LSB_4", "LSB_4", "F5", "F5", "Adaptive_threshold"]
    pattern_index = 0

    print('Length of binary data in (Bytes) = ', len(binary_data))

    counter = 0
    while byte_index < len(binary_data) and counter < frames_needed:
        current_algorithm = frame_pattern[pattern_index]
        capacity = capacities[current_algorithm]
        chunk = binary_data[byte_index:byte_index + capacity]     
        if chunk:  # Only add non-empty chunks
            chunks.append(chunk)
            counter += 1
            print(f"Chunk {counter} ({current_algorithm}) saved successfully.")
        byte_index += capacity
        pattern_index = (pattern_index + 1) % len(frame_pattern)

    end_time = time.time()
    print(f"Time to process binary data: {end_time - start_time:.4f} seconds")
    return chunks

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
            output_path = os.path.join(output_folder, f'chunk_{i:05d}.bin')
            with open(output_path, 'wb') as file:
                file.write(chunk)

    end_time = time.time()
    print(f"Time to save chunks to files: {end_time - start_time:.4f} seconds")

def main(binary_file_path, capacities_file_path, frames_needed_file_path, output_folder):
    binary_data = read_binary_file(binary_file_path)
    capacities = read_capacities_file(capacities_file_path)
    frames_needed = read_frames_needed(frames_needed_file_path)

    chunks = split_binary_data(binary_data, capacities, frames_needed)
    save_chunks_to_files(chunks, output_folder)
    print(f"Chunks have been saved to {output_folder}")
    delete_bin_file(binary_file_path)


# Example usage:
binary_file_path = r'encrypted_data.bin'
capacities_file_path = r'User_Output_Statistics\Algorithms_max_Capacity.txt'
frames_needed_file_path = r'User_Output_Statistics\frames_needed.txt'
output_folder = r'input_frames_folder_data'

main(binary_file_path, capacities_file_path, frames_needed_file_path, output_folder)
