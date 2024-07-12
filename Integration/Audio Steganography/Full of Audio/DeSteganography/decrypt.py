from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64
import os

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
    
def decrypt_file(input_file_path, output_file_path, key):
    # Decode the base64 encoded key
    key = base64.b64decode(key)
    
    # Read the input file
    with open(input_file_path, 'rb') as f:
        iv = f.read(16)
        encrypted_data = f.read()
    
    # Create a cipher object
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    # Unpad the data
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    # Write the decrypted data to the output file
    with open(output_file_path, 'wb') as f:
        f.write(data)

if __name__ == '__main__':
    # Load the key from a file
    key_file_path = r'User_Input\encryption_key.txt'
    with open(key_file_path, 'r') as key_file:
        key = key_file.read()
    in_file_path = 'extracted_folder_data.bin'
    out_file_path = 'decrypted_folder_data.bin'   
    decrypt_file(in_file_path,out_file_path,key)
    delete_bin_file(in_file_path)
