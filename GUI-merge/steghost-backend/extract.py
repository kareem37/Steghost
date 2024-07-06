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
    theta_q_padded = np.pad(theta_q, ((0, N_pad), (0, N_pad)), mode='constant')
    
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
    if secret_message_length* 3 > max_capacity_bits:
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

def bit_string_to_file(bit_string, output_path):
    if len(bit_string) % 8 != 0:
        raise ValueError("Bit string length should be a multiple of 8.")
    byte_array = bytearray(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8))
    with open(output_path, 'wb') as file:
        file.write(byte_array)

def file_to_bit_string(file_path):
    with open(file_path, 'rb') as file:
        byte_data = file.read()
    binary_string = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_string

def pvd_lsb_extract(image, BOI, message_length):
    bit_data = []
    data_index = 0
    extracted_message_length = message_length

    M, N = image.shape

    for i in range(0, M, 2):
        for j in range(0, N, 2):
            if i + 2 > M or j + 2 > N:
                continue  # Skip blocks that are out of bounds
            if BOI[i // 2, j // 2] and data_index < extracted_message_length:
                block = image[i:i+2, j:j+2].astype(np.int32)
                if data_index + 2 <= extracted_message_length:
                    p1, p2 = block[0, 1], block[1, 0]
                    diff = p2 - p1
                    secret_value = abs(diff)
                    secret_bits = format(secret_value, '02b')
                    bit_data.extend(secret_bits)
                    data_index += 2
                for x in range(2):
                    for y in range(2):
                        if (x, y) != (0, 1) and (x, y) != (1, 0) and data_index < extracted_message_length:
                            pixel_value = block[x, y]
                            lsb_value = pixel_value & 1
                            bit_data.append(str(lsb_value))
                            data_index += 1

    bit_string = ''.join(bit_data)

    if len(bit_string) < extracted_message_length:
        print(f"Warning: Extracted message is shorter than expected. Extracted length: {len(bit_string)}, Expected length: {extracted_message_length}")
    else:
        print(f"All data extracted successfully. Extracted length: {len(bit_string)}, Expected length: {extracted_message_length}")

    return bit_string[:message_length]

def verify_data(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
    return data1 == data2

def compare_bit_strings(original, extracted):
    for i in range(len(original)):
        if original[i] != extracted[i]:
            print(f"Mismatch at position {i}: original={original[i]}, extracted={extracted[i]}")
            print(f"Original data surrounding mismatch: {original[i-10:i+10]}")
            print(f"Extracted data surrounding mismatch: {extracted[i-10:i+10]}")
            return False
    return True

def process_rgb_image(image, func, *args):
    channels = list(cv2.split(image))
    results = []
    for channel in channels:
        result = func(channel, *args)
        results.append(result)
    return results

def extract_data_from_channels(embedded_image, BOIs, secret_message_length):
    total_length = secret_message_length
    part_length = total_length // 3
    part_length -= part_length % 8  # Ensure each part length is a multiple of 8

    extracted_bit_strings = []
    channels = list(cv2.split(embedded_image))
    
    for i, channel in enumerate(channels):
        BOI = BOIs[i]
        if i == len(channels) - 1:  # Check if this is the last channel
            extracted_bit_string = pvd_lsb_extract(channel, BOI, total_length - 2 * part_length)
        else:
            extracted_bit_string = pvd_lsb_extract(channel, BOI, part_length)
        extracted_bit_strings.append(extracted_bit_string)
    
    extracted_bit_string = ''.join(extracted_bit_strings)
    return extracted_bit_string[:secret_message_length]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract.py <embedded_image_path> <binary_file_path>")
        sys.exit(1)

    embedded_image_path = sys.argv[1]
    binary_file_path = sys.argv[2]

    # Read the embedded image
    embedded_image = cv2.imread(embedded_image_path)
    if embedded_image is None:
        raise FileNotFoundError(f"Embedded image at path '{embedded_image_path}' could not be loaded. Please check the path and try again.")

    bit_secret_data = file_to_bit_string(binary_file_path)
    secret_message_length = len(bit_secret_data)

    # Compute HOG and find BOI with adaptive thresholding for each channel
    hogs = process_rgb_image(embedded_image, compute_hog)
    BOIs = [find_blocks_of_interest(hog, secret_message_length // 3)[0] for hog in hogs]

    # Extract the bit secret data from each channel
    start = time.time()
    extracted_bit_string = extract_data_from_channels(embedded_image, BOIs, secret_message_length)
    end = time.time()
    print("extraction time =", end - start)

    bit_string_to_file(extracted_bit_string, 'extracted_file_bin.bin')

    # Perform bit-by-bit comparison of the bit strings
    comparison_result = compare_bit_strings(bit_secret_data, extracted_bit_string)
    print("Bit String Comparison Result:", comparison_result)

    # Verify that the contents of the embedded data are the same as the extracted data
    is_verified = verify_data(binary_file_path, 'extracted_file_bin.bin')
    print("Verification Result:", is_verified)
