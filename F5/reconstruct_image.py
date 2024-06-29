import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct


# Step 3: Apply inverse DCT
def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

# Read the quantized DCT coefficients from the text file
stego_encoded_coefficients = np.loadtxt('stego_encoded_coefficients.txt', dtype=int)


reconstructed_image = idct2(stego_encoded_coefficients)
reconstructed_image = np.clip(reconstructed_image, 0, 255)
reconstructed_image = Image.fromarray(reconstructed_image.astype(np.uint8))

# Save or display the gray image
reconstructed_image.show()
reconstructed_image.save('reconstructed_gray_image.png')




