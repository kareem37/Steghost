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

def matrix_encode(message_bits, encoded_pixels):
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

def f5_embed(channel_pixels, message_bits, key ,scenario):
    if scenario == 0  or message_bits == []: # No embedding
        return channel_pixels
    permuted_pixels, permuted_indices = permute_pixels(channel_pixels, key)
    encoded_pixels = permuted_pixels.copy()
    if scenario == 1 : # Partial embedding
        encoded_pixels = matrix_encode(message_bits, encoded_pixels)
    else : # Full embedding
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

def compute_data_size(data_size_array):
    length = int(data_size_array,2)
    #print('length',length)
    return length


def Data_Distributer(pure_data , pure_data_size , max_capacity_per_channel):
    #Scenario 0: No data to embedding into channel
    #Scenario 1: partial embedding of data into channel
    #Scenario 2: Full embedding of data into channel
    #Error = True if pure_data_size > 3* max_capacity_per_channel
    Error = False #
    red_channel_bit_array= []
    green_channel_bit_array= []
    blue_channel_bit_array= []
    if pure_data_size < max_capacity_per_channel:
        red_channel_scenario = 1
        green_channel_scenario = 0
        blue_channel_scenario = 0
        red_channel_bit_array = pure_data
    elif pure_data_size == max_capacity_per_channel:
        red_channel_scenario = 2
        green_channel_scenario = 0
        blue_channel_scenario = 0
        red_channel_bit_array = pure_data
    elif pure_data_size < 2 * max_capacity_per_channel:
        red_channel_scenario = 2
        green_channel_scenario = 1
        blue_channel_scenario = 0
        red_channel_bit_array = pure_data[:max_capacity_per_channel]
        green_channel_bit_array = pure_data[max_capacity_per_channel:]
    elif pure_data_size == 2 * max_capacity_per_channel:
        red_channel_scenario = 2
        green_channel_scenario = 2
        blue_channel_scenario = 0
        red_channel_bit_array = pure_data[:max_capacity_per_channel]
        green_channel_bit_array = pure_data[max_capacity_per_channel:]        
    elif pure_data_size < 3 * max_capacity_per_channel:
        red_channel_scenario = 2
        green_channel_scenario = 2
        blue_channel_scenario = 1
        red_channel_bit_array = pure_data[:max_capacity_per_channel]
        green_channel_bit_array = pure_data[max_capacity_per_channel:2 * max_capacity_per_channel]
        blue_channel_bit_array = pure_data[2 * max_capacity_per_channel:]
    elif pure_data_size == 3 * max_capacity_per_channel:
        red_channel_scenario = 2
        green_channel_scenario = 2
        blue_channel_scenario = 2
        red_channel_bit_array = pure_data[:max_capacity_per_channel]
        green_channel_bit_array = pure_data[max_capacity_per_channel:2 * max_capacity_per_channel]
        blue_channel_bit_array = pure_data[2 * max_capacity_per_channel:]
    else:
        Error = True  #Error = Impossible to embed this data into this cover img
    return red_channel_scenario, green_channel_scenario, blue_channel_scenario , red_channel_bit_array, green_channel_bit_array, blue_channel_bit_array , Error  # Return the scenarios, channel_bit_arrays and error status 
    
        
# Example usage
filename = 'data.bin'
bit_array = read_bin_file_to_bits(filename)
pure_data_size = compute_data_size(bit_array[:31])
pure_data = bit_array[31:]

image_path = 'image.png'  # Replace with your image path
red_channel, green_channel, blue_channel ,height, width = get_pixels_array_channels(image_path)
max_capacity_per_channel = height * width

red_channel_scenario, green_channel_scenario, blue_channel_scenario, red_channel_bit_array, green_channel_bit_array, blue_channel_bit_array , Error = Data_Distributer(pure_data, pure_data_size , max_capacity_per_channel)

# ......
# F5
if Error == False: 
    key = 42
    stego_encoded_pixels_red_channel =  f5_embed(red_channel ,red_channel_bit_array , key ,red_channel_scenario  )
    stego_encoded_pixels_green_channel  = f5_embed( green_channel, green_channel_bit_array, key ,green_channel_scenario )
    stego_encoded_pixels_blue_channel = f5_embed( blue_channel, blue_channel_bit_array, key ,blue_channel_scenario )

    # ......
    get_image(stego_encoded_pixels_red_channel, stego_encoded_pixels_green_channel, stego_encoded_pixels_blue_channel, height, width)  # Replace height and width with your image dimensions.   
else: 
    print("Error: Cannot embed this data into this cover image.")


