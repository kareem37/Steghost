import numpy as np
from PIL import Image
from scipy.fftpack import dct, idct

def load_dct_coefficients(filename):
    return np.loadtxt(filename, dtype=int)

def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

# Step 1: Read the input files
original_image = Image.open('image.png')
gray_stego_image = Image.open('reconstructed_gray_image.png')
stego_dct_coefficients = load_dct_coefficients('stego_encoded_coefficients.txt')

# Step 2: Convert the original RGB image to grayscale
original_gray_image = original_image.convert('L')
original_gray_np = np.array(original_gray_image)

# Step 3: Compute the DCT coefficients of the original grayscale image
original_dct_coefficients = dct2(original_gray_np)

# Step 4: Compare the DCT coefficients with the target stego DCT coefficients
if not np.array_equal(original_dct_coefficients, stego_dct_coefficients):
    print("DCT coefficients are not identical. Modifying the image.")

    # Step 5: Create an empty array for the modified grayscale image
    modified_gray_dct = np.copy(original_dct_coefficients)

    # Step 6: Replace the DCT coefficients with the target stego DCT coefficients
    modified_gray_dct = stego_dct_coefficients

    # Step 7: Apply inverse DCT to reconstruct the modified grayscale image
    modified_gray_image = idct2(modified_gray_dct)
    modified_gray_image = np.clip(modified_gray_image, 0, 255).astype(np.uint8)
    modified_gray_pil = Image.fromarray(modified_gray_image)

    # Step 8: Create an empty array for the reconstructed RGB image
    reconstructed_rgb_image_np = np.zeros_like(np.array(original_image), dtype=np.float32)

    # Step 9: Apply the DCT and replace the coefficients for each channel in the original RGB image
    for channel in range(3):
        original_channel = np.array(original_image)[:, :, channel]
        dct_channel = dct2(original_channel)
        dct_channel[:modified_gray_dct.shape[0], :modified_gray_dct.shape[1]] = modified_gray_dct
        reconstructed_channel = idct2(dct_channel)
        reconstructed_rgb_image_np[:, :, channel] = np.clip(reconstructed_channel, 0, 255)

    # Convert the reconstructed image to uint8
    reconstructed_rgb_image_np = reconstructed_rgb_image_np.astype(np.uint8)
    reconstructed_rgb_image = Image.fromarray(reconstructed_rgb_image_np)

    # Save the reconstructed RGB image
    reconstructed_rgb_image.save('reconstructed_rgb_image.png')

    print("Reconstructed RGB image saved as 'reconstructed_rgb_image.png'")
else:
    print("DCT coefficients are identical. No modification needed.")
