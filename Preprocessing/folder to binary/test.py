def read_bin_file(file_path):
    with open(file_path, 'rb') as file:
        byte_data = file.read()
    return byte_data

def convert_to_bit_array(byte_data):
    bit_array = ''.join(format(byte, '08b') for byte in byte_data)
    return bit_array

def main():
    bin_file_path = r'folder_data.bin'
    byte_data = read_bin_file(bin_file_path)
    bit_array = convert_to_bit_array(byte_data)
    print('len(bit_array): ',len(bit_array))
    print('Bit array:', bit_array[:100])


if __name__ == "__main__":
    main()
