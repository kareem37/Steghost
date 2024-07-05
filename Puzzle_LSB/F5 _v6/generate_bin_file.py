import os
import numpy as np

def read_bin_file_to_bits(filename):
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    bit_array = np.unpackbits(byte_array)
    return bit_array

def compute_data_size(data_size_array):
    data_size_str = ''.join(map(str, data_size_array))
    length = int(data_size_str,2)
    #print('length',length, ' bits')
    return length

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

import numpy as np

def update_file_with_length(bit_array, size_in_bits, filename):
    # Convert the length to a 24-bit binary representation
    length_bits = np.binary_repr(size_in_bits, width=24)
    #print('Length bits = ', length_bits)

    # Update the first 24 bits of the file data
    for i in range(24):
        bit_array[i] = int(length_bits[i])
        
    length = compute_data_size(bit_array[:24])
    #print('bit_array[24:length] = ', bit_array[24:length])
    #print('bit_array = ', bit_array)

    # Convert bit array to byte array
    byte_array = bits_to_bytes(bit_array)

    # Write the updated data back to the file
    with open(filename, 'wb') as file:
        file.write(byte_array)

def bits_to_bytes(bit_array):
    # Ensure the bit array length is a multiple of 8
    padded_bit_array = np.pad(bit_array, (0, 8 - len(bit_array) % 8), 'constant')
    # Convert bit array to bytes
    byte_array = np.packbits(padded_bit_array)
    return byte_array

# Example usage

    
# Example usage
filename = 'data.bin'
size_in_bits = 720 * 1280 *3  # Specify the size in bits
generate_random_bin_file(filename, size_in_bits)
print(f"Generated a binary file '{filename}' of size {size_in_bits} bits.")

bit_array = read_bin_file_to_bits(filename)

length = compute_data_size(bit_array[:24])
#print('bit_array[24:length] = ' , bit_array[24:length] )
#print('len(bit_array) = ' , len(bit_array) )
#print('================================================================')
update_file_with_length(bit_array,size_in_bits,filename)
#print('================================================================')
filename = 'data.bin'
bit_array = read_bin_file_to_bits(filename)
length = compute_data_size(bit_array[:24])
#print('bit_array[24:length] = ' , bit_array[24:length] )
#print('len(bit_array) = ' , len(bit_array) )