
import numpy as np

def read_bin_file_to_bits(filename):
    #Read the binary file
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    
    #Convert each byte to its bit representation
    bit_array = np.unpackbits(byte_array)
    
    return bit_array


def permute_coefficients(dct_coefficients, key):
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(dct_coefficients))
    #print(f"Permuted Indices: {permuted_indices}")
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

def adjust_coefficients(encoded_coefficients):
    encoded_coefficients = np.where(encoded_coefficients == 0, 1, encoded_coefficients)
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
    #print(f"Permuted Coefficients: {permuted_coefficients}")
    encoded_coefficients = matrix_encode(message_bits, permuted_coefficients)
    #print(f"Encoded Coefficients: {encoded_coefficients}")
    stego_encoded_coefficients = reorder_coefficients(encoded_coefficients,permuted_indices)
    #print(f"Stego encoded Coefficients: {stego_encoded_coefficients}")
    
    return stego_encoded_coefficients

# Read the quantized DCT coefficients from the text file
loaded_quantized_dct = np.loadtxt('quantized_dct.txt', dtype=int)

shape = loaded_quantized_dct.shape
print(f"Loading DCT Coefficients: {shape}")

# Flatten the array
loaded_quantized_dct = loaded_quantized_dct.flatten()
print(f"Flattened DCT Coefficients: {loaded_quantized_dct.shape}")

# Read bin file
filename = 'data.bin'  #  binary file
bit_array = read_bin_file_to_bits(filename)

key = 42

# Embedding
stego_encoded_coefficients = f5_embed(loaded_quantized_dct, bit_array, key)

# Reshaping

stego_encoded_coefficients = stego_encoded_coefficients.reshape(shape)
print(f"Reshaped Stego Coefficients: {stego_encoded_coefficients.shape}")

# Save the stego_encoded_coefficients to a text file
np.savetxt('stego_encoded_coefficients.txt', stego_encoded_coefficients, fmt='%d')
#print("Stegno encoded Coefficients:", stego_encoded_coefficients)
