def read_bin_file(file_path):
    with open(file_path, 'rb') as file:
        byte_data = file.read()
    return byte_data

def convert_to_bit_array(byte_data):
    bit_array = ''.join(format(byte, '08b') for byte in byte_data)
    return bit_array

def compare_bit_arrays(bit_array1, bit_array2):
    return bit_array1 == bit_array2

def main():
    bin_file_path = r'test\extracted_folder_data.bin'
    target_bit_array = '011101011111011000000011101001100110101011111011001100001011110111110111011110101001101100011111'
    
    byte_data = read_bin_file(bin_file_path)
    bit_array = convert_to_bit_array(byte_data)
    print('len:', len(bit_array)  )
    print('bit_array:', bit_array[:100] + '...')  # Print the first 100 bits for readability.
    if compare_bit_arrays(bit_array, target_bit_array):
        print("The bit arrays are identical.")
    else:
        print("The bit arrays are not identical.")

if __name__ == "__main__":
    main()
