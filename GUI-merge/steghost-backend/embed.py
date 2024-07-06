import sys
import numpy as np
import cv2
from scipy.ndimage import convolve
import time

def compute_gradients(image):
    Kx = np.array([[-1, 1], [-1, 1]])  # 2D kernel for x-gradient
    Ky = np.array([[-1, -1], [1, 1]])  # 2D kernel for y-gradient
    Gx = convolve(image, Kx)
    Gy = convolve(image, Ky)
    return Gx, Gy

def compute_magnitude_and_angle(Gx, Gy):
    G = np.sqrt(Gx**2 + Gy**2)
    theta = np.arctan2(Gy, Gx) * 180 / np.pi  # Convert to degrees
    return G, theta

def normalize_magnitude(G):
    G_max = np.max(G)
    Gn = G / G_max if G_max != 0 else G
    return Gn

def quantize_angle(theta):
    angle_quantization = np.zeros_like(theta)
    theta = np.mod(theta + 180, 180)  # Normalize angles to [0, 180)
    angle_quantization[(theta >= 0) & (theta < 45)] = 1
    angle_quantization[(theta >= 45) & (theta < 90)] = 2
    angle_quantization[(theta >= 90) & (theta < 135)] = 3
    angle_quantization[(theta >= 135) & (theta < 180)] = 4
    return angle_quantization

def compute_hog(image, block_size=2):
    M, N = image.shape
    Gx, Gy = compute_gradients(image)
    G, theta = compute_magnitude_and_angle(Gx, Gy)
    Gn = normalize_magnitude(G)
    theta_q = quantize_angle(theta)
    
    # Ensure M and N are divisible by block_size
    M_pad = (block_size - M % block_size) % block_size
    N_pad = (block_size - N % block_size) % block_size
    Gn_padded = np.pad(Gn, ((0, M_pad), (0, N_pad)), mode='constant')
    theta_q_padded = np.pad(theta_q, ((0, M_pad), (0, N_pad)), mode='constant')
    
    M_padded, N_padded = Gn_padded.shape
    hog = np.zeros((M_padded // block_size, N_padded // block_size, 4))
    
    for i in range(0, M_padded, block_size):
        for j in range(0, N_padded, block_size):
            block_magnitude = Gn_padded[i:i+block_size, j:j+block_size]
            block_angle = theta_q_padded[i:i+block_size, j:j+block_size]
            for q in range(1, 5):
                hog[i // block_size, j // block_size, q - 1] = np.sum(block_magnitude[block_angle == q])
    return hog

def find_blocks_of_interest(hog, secret_message_length, increment=0.01):
    M, N, _ = hog.shape
    total_blocks = (M * N)  # Number of 2x2 blocks
    max_capacity = total_blocks * 4  # Each 2x2 block can store 4 bits
    max_capacity_bits = int(max_capacity *2.5)  # Capacity in bits
    print("max_capacity", max_capacity_bits)
    if secret_message_length*3 > max_capacity_bits :
        raise ValueError(f"Secret message is too large to be embedded in the cover image. Maximum capacity is {max_capacity_bits} bits.")

    T = 0.1  # Starting with a higher initial threshold value
    while T <= 1.0:
        dominant_magnitude = np.max(hog, axis=2)
        BOI = dominant_magnitude > T
        Ne = np.sum(BOI)
        if Ne * 4 >= secret_message_length:
            break
        T += increment
    return BOI, T

def file_to_bit_string(file_path):
    with open(file_path, 'rb') as file:
        byte_data = file.read()
    binary_string = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_string

def pvd_lsb_embed(image, BOI, bit_secret_data):
    data_index = 0
    data_length = len(bit_secret_data)
    
    embedded_image = image.copy()
    M, N = embedded_image.shape

    for i in range(0, M, 2):
        for j in range(0, N, 2):
            if i + 2 > M or j + 2 > N:
                continue  # Skip blocks that are out of bounds
            if BOI[i // 2, j // 2] and data_index < data_length:
                block = embedded_image[i:i+2, j:j+2].astype(np.int32)
                if data_index + 2 <= data_length:
                    p1, p2 = block[0, 1], block[1, 0]
                    diff = p2 - p1
                    secret_bits = bit_secret_data[data_index:data_index + 2]
                    secret_value = int(secret_bits, 2)
                    if diff < 0:
                        secret_value = -secret_value
                    new_p2 = np.clip(p1 + secret_value, 0, 255)
                    block[1, 0] = new_p2
                    data_index += 2
                for x in range(2):
                    for y in range(2):
                        if (x, y) != (0, 1) and (x, y) != (1, 0) and data_index < data_length:
                            pixel_value = block[x, y]
                            lsb_value = int(bit_secret_data[data_index])
                            block[x, y] = (pixel_value & ~1) | lsb_value
                            data_index += 1

                embedded_image[i:i+2, j:j+2] = block.astype(np.uint8)

    if data_index < data_length:
        print(f"Warning: Not all data was embedded. Data index: {data_index}, Data length: {data_length}")
    else:
        print(f"All data embedded successfully. Data index: {data_index}, Data length: {data_length}")

    return embedded_image


def process_rgb_image(image, func, *args):
    channels = list(cv2.split(image))
    results = []
    for channel in channels:
        result = func(channel, *args)
        results.append(result)
    return results

def embed_data_in_channels(image, BOIs, bit_secret_data):
    total_length = len(bit_secret_data)
    part_length = total_length // 3
    part_length -= part_length % 8  # Ensure each part length is a multiple of 8

    bit_secret_data_parts = [
        bit_secret_data[:part_length],
        bit_secret_data[part_length:2 * part_length],
        bit_secret_data[2 * part_length:]
    ]
    embedded_image = image.copy()
    channels = list(cv2.split(embedded_image))
    
    for i, channel in enumerate(channels):
        BOI = BOIs[i]
        channel_embedded = pvd_lsb_embed(channel, BOI, bit_secret_data_parts[i])
        channels[i] = channel_embedded
    
    embedded_image = cv2.merge(channels)
    return embedded_image

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python embed.py <image_path> <data_path>")
        sys.exit(1)

    original_image_path = sys.argv[1]
    binary_file_path = sys.argv[2]

    image = cv2.imread(original_image_path)
    if image is None:
        raise FileNotFoundError(f"Image at path '{original_image_path}' could not be loaded. Please check the path and try again.")

    # Read binary file and convert to bit string
    bit_secret_data = file_to_bit_string(binary_file_path)
    secret_message_length = len(bit_secret_data)

    # Compute HOG and find BOI with adaptive thresholding for each channel
    hogs = process_rgb_image(image, compute_hog)
    BOIs = [find_blocks_of_interest(hog, secret_message_length // 3)[0] for hog in hogs]

    # Embed the bit secret data in each channel
    start = time.time()
    embedded_image = embed_data_in_channels(image, BOIs, bit_secret_data)
    end = time.time()
    
    print("embedding time =", end - start)

    # Save the embedded image
    embedded_image_path = 'uploads/embedded_image.png'
    cv2.imwrite(embedded_image_path, embedded_image)
