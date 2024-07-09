import os
import numpy as np

def read_bits(file, num_bits):
    """Read a specified number of bits from a file and return as a bit string."""
    num_bytes = (num_bits + 7) // 8  # Calculate the number of bytes needed
    data = file.read(num_bytes)
    bit_string = ''.join(f'{byte:08b}' for byte in data)
    return bit_string[:num_bits]

def compare_bin_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        
        # Read the first 24 bits from both files
        first_24_bits_file1 = read_bits(f1, 24)
        print ('first_24_bits_file1:',first_24_bits_file1)
        first_24_bits_file2 = read_bits(f2, 24)
        print ('first_24_bits_file2:',first_24_bits_file2)
        
        if first_24_bits_file1 != first_24_bits_file2:
            print(f"The first 24 bits of {file1} and {file2} are different.")
            return None
        
        # Convert the 24-bit binary string to an integer size
        size_bits = first_24_bits_file1
        size = int(size_bits, 2)
        print(f"Size extracted from the first 24 bits of {file1} and {file2}: {size} bits")

        bits_file1 = read_bits(f1, size)
        bits_file2 = read_bits(f2, size)
        
        remaining_bits = size - 24
        remaining_bytes = (remaining_bits + 7) // 8
        
        diff_bits_count = 0
        chunk_size = 1024  # Adjust the chunk size if necessary
        
        while remaining_bits > 0:
            chunk_bits = min(chunk_size * 8, remaining_bits)
            chunk_bytes = (chunk_bits + 7) // 8
            
            data1 = f1.read(chunk_bytes)
            data2 = f2.read(chunk_bytes)
            
            if not data1 or not data2:
                diff_bits_count += (len(data1) if data1 else 0) * 8
                diff_bits_count += (len(data2) if data2 else 0) * 8
                break
            
            for byte1, byte2 in zip(data1, data2):
                differing_bits = bin(byte1 ^ byte2).count('1')
                diff_bits_count += differing_bits
            
            remaining_bits -= chunk_bits
        
        if diff_bits_count == 0:
            print(f"The files {file1} and {file2} are identical.")
        else:
            print(f"The files {file1} and {file2} differ by {diff_bits_count} bits.")
        return diff_bits_count

def compare_folders(folder1, folder2):
    files1 = sorted([f for f in os.listdir(folder1) if f.endswith('.bin')])
    files2 = sorted([f for f in os.listdir(folder2) if f.endswith('.bin')])

    if len(files1) != len(files2):
        print("The folders contain a different number of files.")
        return

    total_diff_bits = 0

    for file1, file2 in zip(files1, files2):
        path1 = os.path.join(folder1, file1)
        path2 = os.path.join(folder2, file2)
        diff_bits = compare_bin_files(path1, path2)
        if diff_bits is not None:
            total_diff_bits += diff_bits
    
    print(f"Total differing bits across all files: {total_diff_bits}")

# Example usage
folder1 = 'input_frames_folder_data'
folder2 = 'output_frames_folder_data'
compare_folders(folder1, folder2)
