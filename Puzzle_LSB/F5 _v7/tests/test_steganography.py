import unittest
from F5_Steganography import read_bin_file_to_bits
import numpy as np

class TestSteganography(unittest.TestCase):
    
    def test_read_bin_file_to_bits(self):
        bit_array = read_bin_file_to_bits('test_data.bin')
        self.assertIsInstance(bit_array, np.ndarray)
    
