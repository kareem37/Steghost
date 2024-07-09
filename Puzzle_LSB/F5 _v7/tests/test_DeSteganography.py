import unittest
from extraction import compute_data_size, extract_actual_data_bits

class TestExtraction(unittest.TestCase):
    
    def test_compute_data_size(self):
        data_size_array = [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1]
        self.assertEqual(compute_data_size(data_size_array), 123456)
    
    def test_extract_actual_data_bits(self):
        extracted_bits = [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        actual_data_bits = extract_actual_data_bits(extracted_bits, compute_data_size)
        self.assertEqual(actual_data_bits, extracted_bits[:compute_data_size(extracted_bits[:24])])

if __name__ == '__main__':
    unittest.main()
