import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
from PIL import Image
import time
import os
import argparse

def decode_binary_image(encoded_image_path, output_bin_path):
    start_time = time.time()
    img = Image.open(encoded_image_path)
    width, height = img.size
    pixels = np.array(img, dtype=np.uint8)
    binary_message = np.zeros(width * height * 3 * 2, dtype=np.uint8)  # Max possible size

    mod = SourceModule("""
    __global__ void decode_kernel(unsigned char *pixels, unsigned char *binary_message, int message_length) {
        int idx = blockIdx.x * blockDim.x + threadIdx.x;
        int bit_idx = idx * 6;
        if (bit_idx < message_length) {
            for (int n = 0; n < 3; ++n) {
                unsigned char channel = pixels[idx * 3 + n];
                binary_message[bit_idx + n * 2 + 0] = (channel >> 1) & 0x01;
                binary_message[bit_idx + n * 2 + 1] = channel & 0x01;
            }
        }
    }
    """)

    pixels_gpu = cuda.mem_alloc(pixels.nbytes)
    binary_gpu = cuda.mem_alloc(binary_message.nbytes)

    cuda.memcpy_htod(pixels_gpu, pixels)
    
    block_size = 512
    grid_size = (width * height + block_size - 1) // block_size

    decode_kernel = mod.get_function("decode_kernel")
    decode_kernel(pixels_gpu, binary_gpu, np.int32(len(binary_message)), block=(block_size, 1, 1), grid=(grid_size, 1, 1))

    cuda.memcpy_dtoh(binary_message, binary_gpu)

    # Extract message length
    length_binary = ''.join(map(str, binary_message[:32]))
    message_length = int(length_binary, 2)

    binary_message = binary_message[32:32 + message_length]

    # Convert the binary message to bytes
    binary_data = int(''.join(map(str, binary_message[:message_length])), 2).to_bytes((message_length + 7) // 8, byteorder='big')

    with open(output_bin_path, 'wb') as file:
        file.write(binary_data)

    end_time = time.time()
    decoding_time = end_time - start_time

    return "Decoding completed successfully.", decoding_time

# if _name_ == "_main_":
#     parser = argparse.ArgumentParser(description="Decode a binary file from an image using CUDA.")
#     parser.add_argument("encoded_image_path", type=str, help="Path to the encoded image")
#     parser.add_argument("output_bin_path", type=str, help="Path to save the decoded binary file")
    
#     args = parser.parse_args()

#     result, decoding_time = decode_binary_image(args.encoded_image_path, args.output_bin_path)
#     print(result)
#     print("Decoding time:", decoding_time, "seconds")
# #python your_script_name.py encoded_image.png decoded_message.bin

if __name__ == "__main__":
    encoded_image_path = 'Stego_image.png'
    output_bin_path= 'extracted_data.bin'
    
    result, decoding_time = decode_binary_image(encoded_image_path, output_bin_path)
    print(result)
    print("Decoding time:", decoding_time, "seconds")