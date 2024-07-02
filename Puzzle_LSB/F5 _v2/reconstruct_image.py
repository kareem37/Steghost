import numpy as np
from PIL import Image
from scipy.fftpack import  idct

# Function to apply inverse DCT
def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

# Function to reconstruct a channel from its DCT coefficients
def reconstruct_channel(channel_name):
    # Read the quantized DCT coefficients from the text file
    stego_encoded_coefficients = np.loadtxt(f'stego_encoded_coefficients_{channel_name}.txt', dtype=int)
    
    # Apply inverse DCT to reconstruct the channel
    reconstructed_channel = idct2(stego_encoded_coefficients)
    reconstructed_channel = np.clip(reconstructed_channel, 0, 255)
    
    return reconstructed_channel

# Reconstruct each channel
reconstructed_r = reconstruct_channel('r')
reconstructed_g = reconstruct_channel('g')
reconstructed_b = reconstruct_channel('b')

# Combine the channels to form the final RGB image
reconstructed_rgb_image = np.stack((reconstructed_r, reconstructed_g, reconstructed_b), axis=-1)

# Convert to uint8 and create an image
reconstructed_rgb_image = Image.fromarray(reconstructed_rgb_image.astype(np.uint8))

# Save or display the RGB image
reconstructed_rgb_image.show()
reconstructed_rgb_image.save('reconstructed_rgb_image.png')

print("Reconstructed RGB image saved as 'reconstructed_rgb_image.png'")
