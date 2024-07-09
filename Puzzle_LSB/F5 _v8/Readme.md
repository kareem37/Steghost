# F5 Steganography

This project implements F5 steganography to embed binary data into an image.

## Requirements
- numpy
- Pillow

## Usage
1. Prepare a binary file (`data.bin`) containing the data to embed.
2. Prepare an image file (`image.png`) to use as the cover image.
3. choose int Key number: (`key`) ,default : 23
4. choose int data_bit_count number: (`data_bit_count`) ,default : 24
5. Run the script:
    ```bash
    python F5_Steganography.py
    ```

## Modules
- **data_reader**: Reading binary data and image pixels.
- **pixel_permutation**: Permutation and reverse permutation of pixels.
- **encoding**: Encoding and embedding logic.
- **image_reconstruction**: Reconstructing and saving the image.
- **steganography**: Main steganography logic.

## Testing
Unit tests can be added to ensure the functionality of individual components.

----

# F5 DeSteganography Data Extraction

This project extracts hidden data from a stego image using F5 steganography.

## Requirements
- numpy
- Pillow

## Usage
1. Prepare the stego image file (`steganography_image.png`) containing the hidden data.
2. choose int Key number: (`key`) ,default : 23
3. choose int data_bit_count number: (`data_bit_count`) ,default : 24
4. Run the main script:
    ```bash
    python F5_DeSteganography.py
    ```

## Modules
- **image_processing**: Functions for reading image data and reshaping channels.
- **permutation**: Functions for permuting pixels.
- **extraction**: Functions for extracting message bits and computing data size.
- **bit_operations**: Functions for converting bits to bytes and saving to a binary file.
- **main**: Main script for orchestrating the extraction process and logging time complexity.

## Testing
Unit tests can be added to ensure the functionality of individual components.
