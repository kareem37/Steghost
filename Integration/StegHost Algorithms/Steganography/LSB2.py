import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
from PIL import Image
import time
import argparse

def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)
    return binary_string

def encode_binary_image(cover_image_path, binary_message, output_image_path):
    start_time = time.time()
    img = Image.open(cover_image_path)
    width, height = img.size
    pixels = np.array(img, dtype=np.uint8)
    
    # Encode the length of the binary message first (fixed 32 bits for simplicity)
    message_length = len(binary_message)
    length_binary = format(message_length, '032b')  # 32 bits for the length
    full_binary = length_binary + binary_message
    
    full_binary = np.array([int(bit) for bit in full_binary], dtype=np.uint8)
    
    mod = SourceModule("""
    __global__ void encode_kernel(unsigned char *pixels, unsigned char *full_binary, int message_length) {
        int idx = blockIdx.x * blockDim.x + threadIdx.x;
        int bit_idx = idx * 6;
        if (bit_idx < message_length) {
            for (int n = 0; n < 3; ++n) {
                unsigned char channel = pixels[idx * 3 + n];
                unsigned char mask = 0xFC;
                unsigned char new_bits = (full_binary[bit_idx + n * 2 + 0] << 1) |
                                         full_binary[bit_idx + n * 2 + 1];
                pixels[idx * 3 + n] = (channel & mask) | new_bits;
            }
        }
    }
    """)
    
    pixels_gpu = cuda.mem_alloc(pixels.nbytes)
    binary_gpu = cuda.mem_alloc(full_binary.nbytes)
    
    cuda.memcpy_htod(pixels_gpu, pixels)
    cuda.memcpy_htod(binary_gpu, full_binary)
    
    block_size = 512
    grid_size = (width * height + block_size - 1) // block_size
    
    encode_kernel = mod.get_function("encode_kernel")
    encode_kernel(pixels_gpu, binary_gpu, np.int32(len(full_binary)), block=(block_size, 1, 1), grid=(grid_size, 1, 1))
    
    cuda.memcpy_dtoh(pixels, pixels_gpu)
    
    encoded = Image.fromarray(pixels)
    encoded.save(output_image_path)
    
    end_time = time.time()
    encoding_time = end_time - start_time
    
    return "Encoding completed successfully.", encoding_time

if __name__ == "__main__":
    cover_image_path = 'image.png'
    bin_file_path = 'data.bin'
    output_image_path = 'Stego_image.png'
    
    binary_message = read_binary_file(bin_file_path)
    result, encoding_time = encode_binary_image(cover_image_path, binary_message, output_image_path)
    print(result)
    print("Encoding time:", encoding_time, "seconds")