
import numpy as np
from PIL import Image

def get_pixels_array_channels(image_path):
    with Image.open(image_path) as image:
        height, width = image.height, image.width
        image = image.convert("RGB")
        pixels = np.array(image)
        red_channel = pixels[:, :, 0].flatten()
        green_channel = pixels[:, :, 1].flatten()
        blue_channel = pixels[:, :, 2].flatten()
    return red_channel, green_channel, blue_channel , height, width

def permute_pixels(channel_pixels, key):
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(channel_pixels))
    permuted_pixels = channel_pixels[permuted_indices]
    return permuted_pixels, permuted_indices

def f5_extract_message(key, stego_encoded_pixels):
    permuted_pixels, _ = permute_pixels(stego_encoded_pixels, key)
    extracted_bits = [coeff % 2 for coeff in permuted_pixels]
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


# Load the Stego RGB image
image_path = 'reconstructed_image.png'
red_channel, green_channel, blue_channel ,height, width = get_pixels_array_channels(image_path)
key = 42

# Extracting
extracted_bits_red_channel = f5_extract_message(key, red_channel)
extracted_bits_green_channel = f5_extract_message(key, green_channel)
extracted_bits_blue_channel = f5_extract_message(key, blue_channel)

#Concatenate
extracted_bits = extracted_bits_red_channel + extracted_bits_green_channel + extracted_bits_blue_channel

# Save the extracted bits to a binary file
filename = 'extracted_data.bin'
save_bits_to_bin_file(extracted_bits, filename)

print(f"Extracted bits saved to {filename}.")
