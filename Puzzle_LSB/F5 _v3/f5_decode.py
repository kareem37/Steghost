
import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

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

def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Load the reconstructed RGB image
reconstructed_rgb_image = Image.open('updated_rgb_image.png')
reconstructed_rgb_np = np.array(reconstructed_rgb_image)

# Convert the RGB image to grayscale
reconstructed_gray_image = reconstructed_rgb_image.convert('L')
reconstructed_gray_np = np.array(reconstructed_gray_image)

# Compute the DCT coefficients of the grayscale image
gray_dct_coefficients = dct2(reconstructed_gray_np)

# Apply np.round to the DCT coefficients
gray_dct_coefficients = np.round(gray_dct_coefficients)

# Convert the DCT coefficients to integers
gray_dct_coefficients = gray_dct_coefficients.astype(int)

# Save the DCT coefficients to a text file
np.savetxt('gray_dct_coefficients.txt', gray_dct_coefficients, fmt='%d')

# Flatten the array for extraction
gray_dct_coefficients_flat = gray_dct_coefficients.flatten()

key = 42

# Extracting
extracted_bits = f5_extract(key, gray_dct_coefficients_flat)

# Save the extracted bits to a binary file
filename = 'extracted_data.bin'
save_bits_to_bin_file(extracted_bits, filename)

print(f"Extracted bits saved to {filename}.")
