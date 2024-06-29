import numpy as np

def permute_coefficients(dct_coefficients, key):
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(dct_coefficients))
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

def extract_and_save_bits(channel_name, key):
    # Read the quantized DCT coefficients from the text file
    stego_encoded_coefficients = np.loadtxt(f'stego_encoded_coefficients_{channel_name}.txt', dtype=int)
    
    # Flatten the array
    stego_encoded_coefficients = stego_encoded_coefficients.flatten()
    
    # Extracting
    extracted_bits = f5_extract(key, stego_encoded_coefficients)
    
    return extracted_bits

key = 42

# Extract bits from each channel
extracted_bits_r = extract_and_save_bits('r', key)
extracted_bits_g = extract_and_save_bits('g', key)
extracted_bits_b = extract_and_save_bits('b', key)

# Combine extracted bits from all channels
extracted_bits_combined = extracted_bits_r + extracted_bits_g + extracted_bits_b

# Save the combined bits to a binary file
filename = 'extracted_data.bin'
save_bits_to_bin_file(extracted_bits_combined, filename)

print(f"Extracted bits saved to {filename}.")
