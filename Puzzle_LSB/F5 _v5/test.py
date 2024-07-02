import numpy as np

'''
2) human_readable_size Function
Input: int size of file in Bytes and # of decimal_places to be used
Algorithm: Convert bytes to a human-readable string like KB, MB, GB, etc.
Output: human_readable_size as String
Returns: human_readable_size as String
'''
def human_readable_size(size, decimal_places=2):
  """
  
  """
  if size < 1024:
    return f"{size} bytes"
  elif size < 1024 * 1024:
    return f"{size / 1024:.{decimal_places}f} KB"
  elif size < 1024 * 1024 * 1024:
    return f"{size / (1024 * 1024):.{decimal_places}f} MB"
  else:
    return f"{size / (1024 * 1024 * 1024):.{decimal_places}f} GB"
  
def read_bin_file_to_bits(filename):
    with open(filename, 'rb') as file:
        byte_array = np.frombuffer(file.read(), dtype=np.uint8)
    bit_array = np.unpackbits(byte_array)
    return bit_array

filename = 'data.bin'
bit_array = read_bin_file_to_bits(filename)
data_size = bit_array[:31]
for i in range(31):
    data_size[i] = 1

# Convert the bit array to a string
data_size_str = ''.join(map(str, data_size))
length = int(data_size_str, 2)

print('length', length)
str_size = human_readable_size(length)
print('String size:', str_size)
