import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

# Step 1: Read the image and convert to grayscale
image = Image.open('reconstructed_gray_image.png')
image_np = np.array(image)

# Step 2: Apply DCT
def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

dct_coefficients = dct2(image_np)

# Apply the quantization matrix to DCT coefficients
quantized_dct = np.round(dct_coefficients)

# Convert quantized DCT coefficients to integers
quantized_dct = quantized_dct.astype(int)

# Save the flattened quantized DCT coefficients to a text file
np.savetxt('gray_stego_quantized_dct.txt', quantized_dct, fmt='%d')
