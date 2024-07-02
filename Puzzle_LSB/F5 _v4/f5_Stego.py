import numpy as np
from PIL import Image

def read_bin_file_to_bits(filename):
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    bit_array = np.unpackbits(byte_array)
    return bit_array

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

def matrix_encode(message_bits, permuted_pixels):
    encoded_pixels = permuted_pixels.copy()
    for i, bit in enumerate(message_bits):
        if encoded_pixels[i] % 2 != bit:
            encoded_pixels[i] ^= 1  # Toggle the least significant bit
    return encoded_pixels 

def reverse_permute_pixels(permuted_pixels, permuted_indices):
    #Create an array to hold the reordered pixels
    original_pixels = np.zeros_like(permuted_pixels)
    
    #Sort the permuted indices to get the original order
    inverse_permutation = np.argsort(permuted_indices)
    
    #Reorder the permuted pixels according to the original order
    original_pixels = permuted_pixels[inverse_permutation]
    
    return original_pixels

def f5_embed(channel_pixels, message_bits, key):
    permuted_pixels, permuted_indices = permute_pixels(channel_pixels, key)
    encoded_pixels = matrix_encode(message_bits, permuted_pixels)
    stego_encoded_pixels = reverse_permute_pixels(encoded_pixels, permuted_indices)
    return stego_encoded_pixels

def get_image(red_channel, green_channel, blue_channel , height, width):
    # Reshape the flattened channels back to their original shape
    red_channel_reshaped = red_channel.reshape((height, width))
    green_channel_reshaped = green_channel.reshape((height, width))
    blue_channel_reshaped = blue_channel.reshape((height, width))

    # Stack the channels to get the original image array
    reconstructed_array = np.stack((red_channel_reshaped, green_channel_reshaped, blue_channel_reshaped), axis=-1)
    
    print("Reconstructed array shape:", reconstructed_array.shape)  

    # Convert the NumPy array back to an image
    reconstructed_image = Image.fromarray(reconstructed_array.astype('uint8'), 'RGB')
    reconstructed_image.show()  # Display the image
    reconstructed_image.save('reconstructed_image.png')  # Save the image


# Example usage
filename = 'data.bin'
bit_array = read_bin_file_to_bits(filename)

image_path = 'image.png'  # Replace with your image path
red_channel, green_channel, blue_channel ,height, width = get_pixels_array_channels(image_path)
max_capacity_per_channel = height * width

# ......
# F5
key = 42
stego_encoded_pixels_red_channel =  f5_embed(red_channel, bit_array[0:max_capacity_per_channel], key)
stego_encoded_pixels_green_channel  = f5_embed( green_channel, bit_array[max_capacity_per_channel:max_capacity_per_channel*2], key)
stego_encoded_pixels_blue_channel = f5_embed( blue_channel, bit_array[max_capacity_per_channel*2:max_capacity_per_channel*3], key)

# ......
get_image(stego_encoded_pixels_red_channel, stego_encoded_pixels_green_channel, stego_encoded_pixels_blue_channel, height, width)  # Replace height and width with your image dimensions.



