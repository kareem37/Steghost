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
        first_25_bits_file1 = read_bits(f1, 24)
        first_25_bits_file2 = read_bits(f2, 24)
        
        if first_25_bits_file1 != first_25_bits_file2:
            print("The first 24 bits of the files are different.")
            return None
        
        # Convert the 24-bit binary string to an integer size
        size_bits = first_25_bits_file1
        size = int(size_bits, 2)
        print(f"Size extracted from the first 24 bits: {size} bits")

        bits_file1 = read_bits(f1, size)
        #print('bits_file1:', bits_file1)
        bits_file2 = read_bits(f2, size)
        #print('bits_file2:', bits_file1)
                
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
            print("The files are identical.")
        else:
            print(f"The files differ by {diff_bits_count} bits.")
        return diff_bits_count

# Example usage
file1 = r'folder_data.bin'
file2 = r'extracted_folder_data.bin'
compare_bin_files(file1, file2)
