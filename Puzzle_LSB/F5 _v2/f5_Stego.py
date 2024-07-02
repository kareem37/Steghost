
import numpy as np

def read_bin_file_to_bits(filename):
    # Read the binary file
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    
    # Convert each byte to its bit representation
    bit_array = np.unpackbits(byte_array)
    
    return bit_array

def permute_coefficients(dct_coefficients, key):
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(dct_coefficients))
    permuted_coefficients = dct_coefficients[permuted_indices]
    return permuted_coefficients, permuted_indices

def matrix_encode(message_bits, permuted_coefficients):
    encoded_coefficients = permuted_coefficients.copy()
    for i, bit in enumerate(message_bits):
        if encoded_coefficients[i] % 2 != bit:
            if encoded_coefficients[i] > 0:
                encoded_coefficients[i] -= 1
            else:
                encoded_coefficients[i] += 1
    return encoded_coefficients


def reorder_coefficients(encoded_coefficients, permuted_indices):
    # Create an array to hold the reordered coefficients
    stego_encoded_coefficients = np.zeros_like(encoded_coefficients)
    
    # Sort the permuted indices to get the original order
    inverse_permutation = np.argsort(permuted_indices)
    
    # Reorder the encoded coefficients according to the original order
    stego_encoded_coefficients = encoded_coefficients[inverse_permutation]
    
    return stego_encoded_coefficients

def f5_embed(dct_coefficients, message_bits, key):
    permuted_coefficients, permuted_indices = permute_coefficients(dct_coefficients, key)
    encoded_coefficients = matrix_encode(message_bits, permuted_coefficients)
    stego_encoded_coefficients = reorder_coefficients(encoded_coefficients, permuted_indices)
    return stego_encoded_coefficients

# Function to load and process the quantized DCT coefficients for a given channel
def process_channel(channel_name, message_bits, key,channel_index):
    # Read the quantized DCT coefficients from the text file
    loaded_quantized_dct = np.loadtxt(f'quantized_dct_{channel_name}.txt', dtype=int)
    
    shape = loaded_quantized_dct.shape
    print(f"Loading DCT Coefficients for {channel_name} channel: {shape}")
    Max_Capacity = shape[0] * shape[1]
    #assert message_bits.size <= Max_Capacity, "Message too long for the selected channel."
    print(f"Max_Capacity for {channel_name} channel:  {Max_Capacity} ")
    
    # Flatten the array
    loaded_quantized_dct = loaded_quantized_dct.flatten()
    print(f"Flattened DCT Coefficients for {channel_name} channel: {loaded_quantized_dct.shape}")
    
    # Embedding
    stego_encoded_coefficients = f5_embed(loaded_quantized_dct, message_bits[channel_index * Max_Capacity : (channel_index + 1) * Max_Capacity], key)
    
    # Reshaping
    stego_encoded_coefficients = stego_encoded_coefficients.reshape(shape)
    print(f"Reshaped Stego Coefficients for {channel_name} channel: {stego_encoded_coefficients.shape}")
    
    # Save the stego_encoded_coefficients to a text file
    np.savetxt(f'stego_encoded_coefficients_{channel_name}.txt', stego_encoded_coefficients, fmt='%d')
    print(f"Stego encoded coefficients saved for {channel_name} channel.")

# Read the binary file containing the message
filename = 'data.bin'  # binary file
bit_array = read_bin_file_to_bits(filename)

# Define the key for the permutation
key = 42

# Process each channel independently
process_channel('r', bit_array, key, 0)
process_channel('g', bit_array, key, 1)
process_channel('b', bit_array, key, 2)

print("Processed all channels.")
