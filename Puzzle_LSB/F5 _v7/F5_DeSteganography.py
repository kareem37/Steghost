'''
imports
'''
import numpy as np
from PIL import Image
import time

'''
help module
'''
def clear_time_complexity_log(file_name):
    with open(file_name, "w") as f:
        f.write("")
        
def log_time_complexity(message,file_name):
    """Log the Time Complexity of each Function call."""    
    with open(file_name, "a") as f:
        f.write(message + "\n")
        
def compute_data_size(data_size_array,DeStego_Time_file):
    """Compute the size of data to be hidden."""
    start_time = time.time()
    data_size_str = ''.join(map(str, data_size_array))
    length = int(data_size_str, 2)
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"compute_data_size execution time: {execution_time:.6f} seconds",DeStego_Time_file)
    return length, execution_time

'''
bit_operations module
'''
def bits_to_bytes(bits, DeStego_Time_file):
    """Convert a list of bits to bytes."""
    start_time = time.time()
    extra_bits = len(bits) % 8
    if extra_bits != 0:
        bits.extend([0] * (8 - extra_bits))
    bit_array = np.array(bits, dtype=np.uint8)
    byte_array = np.packbits(bit_array)
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"bits_to_bytes execution time: {execution_time:.6f} seconds", DeStego_Time_file)
    return byte_array, execution_time

def save_bits_to_bin_file(bits, filename, DeStego_Time_file):
    """Save bits as a binary file."""
    byte_array, execution_time0 = bits_to_bytes(bits,DeStego_Time_file)
    start_time = time.time()
    with open(filename, 'wb') as file:
        file.write(byte_array)
    end_time = time.time()
    execution_time1 = end_time - start_time
    execution_time = execution_time0 - execution_time1
    log_time_complexity(f"save_bits_to_bin_file execution time: {execution_time:.6f} seconds", DeStego_Time_file)
    return execution_time
'''
pixel_permutation module
'''
def permute_pixels(channel_pixels, key, DeStego_Time_file):
    """Permute pixels using a given key."""
    start_time = time.time()
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(channel_pixels))
    permuted_pixels = channel_pixels[permuted_indices]
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"permute_pixels execution time: {execution_time:.6f} seconds", DeStego_Time_file)
    return permuted_pixels, execution_time
'''
extraction module
'''
def f5_extract_message(key, stego_encoded_pixels, DeStego_Time_file):
    """Extract message bits from permuted pixels."""
    permuted_pixels, execution_time0 = permute_pixels(stego_encoded_pixels, key,DeStego_Time_file)
    start_time = time.time()
    extracted_bits = [pixel % 2 for pixel in permuted_pixels]
    end_time = time.time()
    execution_time1 = end_time - start_time
    execution_time = execution_time0 + execution_time1
    log_time_complexity(f"f5_extract_message execution time: {execution_time:.6f} seconds", DeStego_Time_file)
    return extracted_bits, execution_time

def extract_actual_data_bits(extracted_bits, data_bit_count, DeStego_Time_file):
    """Extract the actual data bits based on the data size."""
    start_time = time.time()
    data_size_array = extracted_bits[:data_bit_count]
    end_time = time.time()
    execution_time0 = end_time - start_time
    data_size, execution_time1 = compute_data_size(data_size_array, DeStego_Time_file)
    start_time = time.time()
    actual_bits = extracted_bits[24:data_size]
    end_time = time.time()
    execution_time2 = end_time - start_time
    execution_time = execution_time0 + execution_time1 + execution_time2
    log_time_complexity(f"extract_actual_data_bits execution time: {execution_time:.6f} seconds", DeStego_Time_file)
    return actual_bits, execution_time
'''
image_processing module
'''
def get_pixels_array_channels(image_path, DeStego_Time_file):
    """Extract RGB channels from image."""
    start_time = time.time()
    with Image.open(image_path) as image:
        height, width = image.height, image.width
        image = image.convert("RGB")
        pixels = np.array(image)
        red_channel = pixels[:, :, 0].flatten()
        green_channel = pixels[:, :, 1].flatten()
        blue_channel = pixels[:, :, 2].flatten()
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"get_pixels_array_channels execution time: {execution_time:.6f} seconds", DeStego_Time_file)
    return red_channel, green_channel, blue_channel, height, width, execution_time
'''
DeSteganography module
'''
def F5_DeSteganography( in_image_path, out_filename, key,data_bit_count,DeStego_Time_file):        
    """F5 Algorithm Steps"""
    clear_time_complexity_log(DeStego_Time_file)
    
    red_channel, green_channel, blue_channel, height, width, execution_time0  = get_pixels_array_channels(in_image_path, DeStego_Time_file)
    
    extracted_bits_red_channel, execution_time1 = f5_extract_message(key, red_channel, DeStego_Time_file)
    extracted_bits_green_channel, execution_time2 = f5_extract_message(key, green_channel, DeStego_Time_file)
    extracted_bits_blue_channel, execution_time3 = f5_extract_message(key, blue_channel, DeStego_Time_file)
    
    start_time_total = time.time()
    extracted_bits = extracted_bits_red_channel + extracted_bits_green_channel + extracted_bits_blue_channel
    end_time_total = time.time()
    execution_time4 = end_time_total - start_time_total
    
    extracted_bits, execution_time5 = extract_actual_data_bits(extracted_bits, data_bit_count, DeStego_Time_file)
    
    execution_time6 = save_bits_to_bin_file(extracted_bits, out_filename, DeStego_Time_file)
    
    execution_time = execution_time0 + execution_time1 + execution_time2 + execution_time3 + execution_time4 + execution_time5 + execution_time6
    
    log_time_complexity(f"Total execution time: {execution_time:.6f} seconds", DeStego_Time_file)
    
    #print(f"Extracted bits saved to {out_filename}.")

# Test usage
if __name__ == "__main__":
    key = 23
    data_bit_count = 24
    in_image_path = 'steganography_image.png'
    out_filename = 'extracted_data.bin'
    DeStego_Time_file = "DeSteganography_time_complexity.txt"
    F5_DeSteganography(in_image_path, out_filename, key,data_bit_count,DeStego_Time_file)
