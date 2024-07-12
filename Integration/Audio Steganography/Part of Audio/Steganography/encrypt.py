import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

def delete_bin_file(file_path):
    """
    Deletes a .bin file if it exists.

    Parameters:
    file_path (str): The path to the .bin file to be deleted.

    Returns:
    bool: True if the file was successfully deleted, False otherwise.
    """
    try:
        if os.path.isfile(file_path) and file_path.endswith('.bin'):
            os.remove(file_path)
            print(f"File {file_path} has been deleted successfully.")
            return True
        else:
            print(f"File {file_path} does not exist or is not a .bin file.")
            return False
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")
        return False
    
def encrypt_file(input_file_path, output_file_path, key_file_path):
    # Generate a random key and IV
    key = os.urandom(32)
    iv = os.urandom(16)
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Read the input file
    with open(input_file_path, 'rb') as f:
        data = f.read()
    
    # Pad the data to make it a multiple of the block size
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Write the IV and the encrypted data to the output file
    with open(output_file_path, 'wb') as f:
        f.write(iv + encrypted_data)
    
    # Save the key as a string in the key file
    with open(key_file_path, 'w') as f:
        f.write(base64.b64encode(key).decode('utf-8'))

if __name__ == '__main__':
    in_binary_file_path = r'folder_data.bin'
    out_encrypted_file_path = r'encrypted_data.bin'
    key_file_path = r'User_Output_Statistics\encryption_key.txt'
    
    encrypt_file(in_binary_file_path, out_encrypted_file_path, key_file_path)
    delete_bin_file(in_binary_file_path)