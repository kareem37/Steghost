import numpy as np
import time


def read_bin_file_to_bits(filename):
    """Read binary file and convert to bit array."""
    start_time = time.time()
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    bit_array = np.unpackbits(byte_array)
    end_time = time.time()
    execution_time = end_time - start_time
    return bit_array, execution_time

data,execution_time = read_bin_file_to_bits('data.bin')
print('execution_time: ',execution_time)