import os
import numpy as np

def generate_random_bin_file(filename, size_in_bits):
    # Calculate the size in bytes
    size_in_bytes = size_in_bits // 8
    
    # Generate random bytes
    random_data = os.urandom(size_in_bytes)
    
    # Write the random bytes to the file
    with open(filename, 'wb') as file:
        file.write(random_data)
    
    # Handle any remaining bits if size_in_bits is not a multiple of 8
    remaining_bits = size_in_bits % 8
    if remaining_bits > 0:
        # Generate a random byte
        random_byte = np.random.randint(0, 256)
        
        # Keep only the required number of bits
        random_byte = random_byte >> (8 - remaining_bits)
        
        # Write the remaining bits to the file
        with open(filename, 'ab') as file:
            file.write(random_byte.to_bytes(1, 'big'))

# Example usage
filename = 'data.bin'
size_in_bits = 720 * 1280 * 3 * 2 - 32# Specify the size in bits
generate_random_bin_file(filename, size_in_bits)
print(f"Generated a binary file '{filename}' of size {size_in_bits} bits.")
