
import numpy as np

def permute_coefficients(dct_coefficients, key):
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(dct_coefficients))
    #print(f"Permuted Indices: {permuted_indices}")
    permuted_coefficients = dct_coefficients[permuted_indices]
    return permuted_coefficients, permuted_indices

def extract_message(key, stego_encoded_coefficients):
    permuted_coefficients, _ = permute_coefficients(stego_encoded_coefficients, key)
    extracted_bits = [coeff % 2 for coeff in permuted_coefficients]
    return extracted_bits


def f5_extract(key, stego_encoded_coefficients):
    extracted_bits = extract_message(key, stego_encoded_coefficients)
    return extracted_bits

def bits_to_bytes(bits):
    # Ensure the length of the bits list is a multiple of 8
    extra_bits = len(bits) % 8
    if extra_bits != 0:
        bits.extend([0] * (8 - extra_bits))  # Pad with zeros
    
    # Convert the list of bits to a NumPy array
    bit_array = np.array(bits, dtype=np.uint8)
    
    # Pack bits into bytes
    byte_array = np.packbits(bit_array)
    
    return byte_array

def save_bits_to_bin_file(bits, filename):
    byte_array = bits_to_bytes(bits)
    
    # Write the byte array to a binary file
    with open(filename, 'wb') as file:
        file.write(byte_array)
        
# Read the quantized DCT coefficients from the text file
stego_encoded_coefficients = np.loadtxt('stego_encoded_coefficients.txt', dtype=int)

# Flatten the array
stego_encoded_coefficients = stego_encoded_coefficients.flatten()

key = 42

# Extracting
extracted_bits = f5_extract(key, stego_encoded_coefficients)
#print("Extracted Bits:", extracted_bits)

filename = 'extracted_data.bin'
save_bits_to_bin_file(extracted_bits, filename)
