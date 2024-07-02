import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

# Step 1: Read the RGB image
image = Image.open('image.png')
image_np = np.array(image)

# Function to apply 2D DCT
def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

# Arrays to store the quantized DCT coefficients for each channel
quantized_dct_r = np.zeros_like(image_np[:, :, 0])
quantized_dct_g = np.zeros_like(image_np[:, :, 1])
quantized_dct_b = np.zeros_like(image_np[:, :, 2])

# Step 2: Apply DCT to each channel and quantize
for channel, quantized_dct in zip(range(3), [quantized_dct_r, quantized_dct_g, quantized_dct_b]):
    dct_coefficients = dct2(image_np[:, :, channel])
    quantized_dct[:, :] = np.round(dct_coefficients).astype(int)

# Step 3: Save the quantized DCT coefficients for each channel to separate text files
np.savetxt('quantized_dct_r.txt', quantized_dct_r, fmt='%d')
np.savetxt('quantized_dct_g.txt', quantized_dct_g, fmt='%d')
np.savetxt('quantized_dct_b.txt', quantized_dct_b, fmt='%d')

print("Quantized DCT coefficients saved for each channel separately.")
