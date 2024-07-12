'''
imports
'''
import argparse
import os
import numpy as np
from PIL import Image
import time
from numba import cuda, njit

'''
help module
'''
def clear_time_complexity_log(file_name):
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    # Create or clear the file
    with open(file_name, "w") as f:
        f.write("")
        
def log_time_complexity(message, file_name):
    """Log the Time Complexity of each Function call."""    
    with open(file_name, "a") as f:
        f.write(message + "\n")
        
def compute_data_size(data_size_array, Stego_Time_file):
    """Compute the size of data to be hidden."""
    start_time = time.time()
    data_size_str = ''.join(map(str, data_size_array))
    length = int(data_size_str, 2)
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"compute_data_size execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return length, execution_time

def append_data_size_to_bit_array(bit_arr, Stego_Time_file):
    start_time = time.time()

    # Compute the length of the bit array
    bit_length = len(bit_arr)
    
    # Convert the length to a 24-bit binary representation
    if bit_length > (2**24 - 1):
        raise ValueError("The bit array is too large to be represented in 24 bits.")
    
    bit_length_bin = format(bit_length, '024b')

    # Ensure bit_length_bin is split into individual bits
    bit_length_bin_array = np.array(list(bit_length_bin), dtype=np.uint8)

    # Append the binary length at the start of the array
    bit_array = np.concatenate((bit_length_bin_array, bit_arr))

    end_time = time.time()
    execution_time = end_time - start_time
    
    log_time_complexity(f"append_data_size_to_bit_array execution time: {execution_time:.6f} seconds", Stego_Time_file)
    
    return bit_array, bit_length, execution_time

'''
data_reader module
'''
def read_bin_file_to_bits(filename, Stego_Time_file):
    """Read binary file and convert to bit array."""
    start_time = time.time()
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    bit_array = np.unpackbits(byte_array)
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"read_bin_file_to_bits execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return bit_array, execution_time

def get_pixels_array_channels(image_path, Stego_Time_file):
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
    log_time_complexity(f"get_pixels_array_channels execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return red_channel, green_channel, blue_channel, height, width, execution_time

'''
pixel_permutation module
'''
# def permute_pixels(channel_pixels, key,Stego_Time_file):
#     """Permute pixels using a given key."""
#     start_time = time.time()
#     np.random.seed(key)
#     permuted_indices = np.random.permutation(len(channel_pixels))
#     permuted_pixels = channel_pixels[permuted_indices]
#     end_time = time.time()
#     execution_time = end_time - start_time
#     log_time_complexity(f"permute_pixels execution time: {execution_time:.6f} seconds",Stego_Time_file)
#     return permuted_pixels, permuted_indices, execution_time

# def reverse_permute_pixels(permuted_pixels, permuted_indices,Stego_Time_file):
#     """Reverse the permutation of pixels."""
#     start_time = time.time()
#     original_pixels = np.zeros_like(permuted_pixels)
#     inverse_permutation = np.argsort(permuted_indices)
#     original_pixels = permuted_pixels[inverse_permutation]
#     end_time = time.time()
#     execution_time = end_time - start_time
#     log_time_complexity(f"reverse_permute_pixels execution time: {execution_time:.6f} seconds",Stego_Time_file)
#     return original_pixels, execution_time

# GPU kernel to permute pixels
@cuda.jit
def permute_pixels_gpu(channel_pixels, permuted_pixels, permuted_indices):
    idx = cuda.grid(1)
    if idx < permuted_pixels.size:
        permuted_pixels[idx] = channel_pixels[permuted_indices[idx]]

# Function to permute pixels using GPU
def permute_pixels(channel_pixels, key, Stego_Time_file):
    """Permute pixels using a given key."""
    start_time = time.time()
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(channel_pixels))
    permuted_pixels = np.zeros_like(channel_pixels)
    
    d_channel_pixels = cuda.to_device(channel_pixels)
    d_permuted_pixels = cuda.device_array_like(permuted_pixels)
    d_permuted_indices = cuda.to_device(permuted_indices)

    threads_per_block = 256
    blocks_per_grid = (len(channel_pixels) + (threads_per_block - 1)) // threads_per_block
    
    permute_pixels_gpu[blocks_per_grid, threads_per_block](d_channel_pixels, d_permuted_pixels, d_permuted_indices)
    permuted_pixels = d_permuted_pixels.copy_to_host()
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"permute_pixels execution time: {execution_time:.6f} seconds", Stego_Time_file)
    
    
    return permuted_pixels, permuted_indices, execution_time

# GPU kernel to reverse permute pixels
@cuda.jit
def reverse_permute_pixels_gpu(permuted_pixels, original_pixels, inverse_permutation):
    idx = cuda.grid(1)
    if idx < original_pixels.size:
        original_pixels[idx] = permuted_pixels[inverse_permutation[idx]]


# Function to reverse permute pixels using GPU
def reverse_permute_pixels(permuted_pixels, permuted_indices, Stego_Time_file):
    """Reverse the permutation of pixels."""
    start_time = time.time()
    original_pixels = np.zeros_like(permuted_pixels)
    inverse_permutation = np.argsort(permuted_indices)
    
    d_permuted_pixels = cuda.to_device(permuted_pixels)
    d_original_pixels = cuda.device_array_like(original_pixels)
    d_inverse_permutation = cuda.to_device(inverse_permutation)

    threads_per_block = 256
    blocks_per_grid = (len(permuted_pixels) + (threads_per_block - 1)) // threads_per_block
    
    reverse_permute_pixels_gpu[blocks_per_grid, threads_per_block](d_permuted_pixels, d_original_pixels, d_inverse_permutation)
    original_pixels = d_original_pixels.copy_to_host()
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"reverse_permute_pixels execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return original_pixels, execution_time


@cuda.jit
def matrix_encode_gpu(message_bits, encoded_pixels):
    idx = cuda.grid(1)
    if idx < message_bits.size:
        if encoded_pixels[idx] % 2 != message_bits[idx]:
            encoded_pixels[idx] ^= 1  # Toggle the least significant bit

def matrix_encode(message_bits, encoded_pixels, Stego_Time_file):
    """Encode message bits into pixel values."""
    start_time = time.time()
    
    d_message_bits = cuda.to_device(message_bits)
    d_encoded_pixels = cuda.to_device(encoded_pixels)

    threads_per_block = 256
    blocks_per_grid = (len(message_bits) + (threads_per_block - 1)) // threads_per_block
    
    matrix_encode_gpu[blocks_per_grid, threads_per_block](d_message_bits, d_encoded_pixels)
    encoded_pixels = d_encoded_pixels.copy_to_host()
    
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"matrix_encode execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return encoded_pixels, execution_time

def Data_Distributer(pure_data, data_size, max_capacity_per_channel, Stego_Time_file):
    """Distribute data across RGB channels."""
    red_channel_scenario = 0
    green_channel_scenario = 0
    blue_channel_scenario = 0
    start_time = time.time()
    Error = False
    red_channel_bit_array = []
    green_channel_bit_array = []
    blue_channel_bit_array = []
    
    if data_size <= max_capacity_per_channel:
        red_channel_scenario = 1 if data_size < max_capacity_per_channel else 2
        green_channel_scenario = 0
        blue_channel_scenario = 0
        red_channel_bit_array = pure_data
    elif data_size <= 2 * max_capacity_per_channel:
        red_channel_scenario = 2
        green_channel_scenario = 1 if data_size < 2 * max_capacity_per_channel else 2
        blue_channel_scenario = 0
        red_channel_bit_array = pure_data[:max_capacity_per_channel]
        green_channel_bit_array = pure_data[max_capacity_per_channel:]
    elif data_size <= 3 * max_capacity_per_channel:
        red_channel_scenario = 2
        green_channel_scenario = 2
        blue_channel_scenario = 1 if data_size < 3 * max_capacity_per_channel else 2
        red_channel_bit_array = pure_data[:max_capacity_per_channel]
        green_channel_bit_array = pure_data[max_capacity_per_channel:2 * max_capacity_per_channel]
        blue_channel_bit_array = pure_data[2 * max_capacity_per_channel:]
    else:
        Error = True
    
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"Data_Distributer execution time: {execution_time:.6f} seconds", Stego_Time_file)
    
    return (red_channel_scenario, green_channel_scenario, blue_channel_scenario, 
            red_channel_bit_array, green_channel_bit_array, blue_channel_bit_array, Error, execution_time)

def f5_embed(channel_pixels, message_bits, key, scenario, Stego_Time_file):
    """Embed message bits into a color channel."""
    start_time = time.time()
    if scenario == 0 or message_bits.size == 0:
        return channel_pixels, 0
    end_time = time.time()
    execution_time0 = end_time - start_time
        
    permuted_pixels, permuted_indices, execution_time1 = permute_pixels(channel_pixels, key, Stego_Time_file)
    encoded_pixels, execution_time2 = matrix_encode(message_bits, permuted_pixels, Stego_Time_file)
    stego_encoded_pixels, execution_time3 = reverse_permute_pixels(encoded_pixels, permuted_indices, Stego_Time_file)
    
    execution_time = execution_time0 + execution_time1 + execution_time2 + execution_time3
    log_time_complexity(f"f5_embed execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return stego_encoded_pixels, execution_time

'''
image_reconstruction module
'''
def get_image(red_channel, green_channel, blue_channel, height, width, out_image_path, Stego_Time_file):
    """Reconstruct and save the image from RGB channels."""
    start_time = time.time()
    red_channel_reshaped = red_channel.reshape((height, width))
    green_channel_reshaped = green_channel.reshape((height, width))
    blue_channel_reshaped = blue_channel.reshape((height, width))

    reconstructed_array = np.stack((red_channel_reshaped, green_channel_reshaped, blue_channel_reshaped), axis=-1)
    reconstructed_image = Image.fromarray(reconstructed_array.astype('uint8'), 'RGB')
    reconstructed_image.save(out_image_path)
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"get_image execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return execution_time

'''
steganography module
'''
def F5_Steganography(filename, in_image_path, out_image_path, key, data_bit_count, Stego_Time_file):        
    """F5 Algorithm Steps"""
    clear_time_complexity_log(Stego_Time_file)
    
    bit_arr, execution_time0 = read_bin_file_to_bits(filename, Stego_Time_file)
    #print( " bit_arr: ", bit_arr)
    bit_array, data_size, execution_time1 = append_data_size_to_bit_array(bit_arr, Stego_Time_file)
    data_size  = data_size + data_bit_count # bit_array size after append_data_size_to_bit_array
    #print( " data_size: ", data_size)
    #print( " bit_array: ", bit_array)
    
    red_channel, green_channel, blue_channel, height, width, execution_time2 = get_pixels_array_channels(in_image_path, Stego_Time_file)
    max_capacity_per_channel = height * width
    
    (red_channel_scenario, green_channel_scenario, blue_channel_scenario, 
     red_channel_bit_array, green_channel_bit_array, blue_channel_bit_array, Error, execution_time3) = Data_Distributer(bit_array, data_size, max_capacity_per_channel, Stego_Time_file)
    
    if not Error:
        stego_encoded_pixels_red_channel, execution_time4 = f5_embed(red_channel, red_channel_bit_array, key, red_channel_scenario, Stego_Time_file)
        stego_encoded_pixels_green_channel, execution_time5 = f5_embed(green_channel, green_channel_bit_array, key, green_channel_scenario, Stego_Time_file)
        stego_encoded_pixels_blue_channel, execution_time6 = f5_embed(blue_channel, blue_channel_bit_array, key, blue_channel_scenario, Stego_Time_file)
        
        execution_time7 = get_image(stego_encoded_pixels_red_channel, stego_encoded_pixels_green_channel, stego_encoded_pixels_blue_channel, height, width, out_image_path, Stego_Time_file)
    else:
        execution_time4 = 0
        execution_time5 = 0
        execution_time6 = 0
        execution_time7 = 0
        print("Error: Cannot embed this data into this cover image.")
    
    execution_time =  execution_time0 + execution_time1 + execution_time2 + execution_time3 + execution_time4 + execution_time5 + execution_time6 + execution_time7 
    log_time_complexity(f"Total execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return Error

# Test usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="F5 Steganography")
    parser.add_argument("--key", type=int, required=True, help="Key for pixel permutation")
    parser.add_argument("--data_bit_count", type=int, required=True, help="Number of bits in the data to be hidden")
    parser.add_argument("--filename", type=str, required=True, help="Path to the binary file containing the data")
    parser.add_argument("--in_image_path", type=str, required=True, help="Path to the input image file")
    parser.add_argument("--out_image_path", type=str, required=True, help="Path to the output image file")
    parser.add_argument("--Stego_Time_file", type=str, required=True, help="Path to the log file for time complexities")
    
    args = parser.parse_args()
    
    F5_Steganography(args.filename, args.in_image_path, args.out_image_path, args.key, args.data_bit_count, args.Stego_Time_file)

# # Test usage
# if __name__ == "__main__":
#     key = 23
#     data_bit_count = 24
#     filename = 'data.bin'
#     in_image_path = 'image.png'
#     out_image_path = 'steganography_image.png'
#     Stego_Time_file = "V2_steganography_time_complexity.txt"
#     F5_Steganography(filename, in_image_path, out_image_path, key, data_bit_count, Stego_Time_file)
