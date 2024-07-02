import numpy as np

def read_bin_file_to_bits(filename):
    # Read the binary file in binary mode
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    
    # Convert each byte to its bit representation
    bit_array = np.unpackbits(byte_array)
    
    return bit_array

def convert_bin_to_txt(bin_filename, txt_filename, num_bits):
    # Read the binary file and get the bit array
    bit_array = read_bin_file_to_bits(bin_filename)
    
    # If the number of bits is not divisible by 8, truncate the array to the desired length
    bit_array = bit_array[:num_bits]
    
    # Convert the bit array to a string
    bit_string = ''.join(bit_array.astype(str))
    
    # Write the bit string to a text file
    with open(txt_filename, 'w') as file:
        file.write(bit_string)

# Example usage:
bin_file_path = 'data.bin'
txt_file_path = 'data.txt'
num_bits = 17  # Specify the exact number of meaningful bits

convert_bin_to_txt(bin_file_path, txt_file_path, num_bits)
print(f"Converted {bin_file_path} to {txt_file_path} with {num_bits} bits.")
