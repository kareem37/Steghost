def compare_bin_files(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        # Read the files in chunks
        chunk_size = 1024  # Adjust the chunk size if necessary
        
        diff_bits_count = 0
        
        while True:
            data1 = f1.read(chunk_size)
            data2 = f2.read(chunk_size)
            
            # If both files are empty at the same time, break
            if not data1 and not data2:
                break
            
            # If one file is empty but the other is not, they are different
            if not data1 or not data2:
                diff_bits_count += len(data1) * 8 if data1 else len(data2) * 8
                break
            
            # Compare the chunks
            for byte1, byte2 in zip(data1, data2):
                differing_bits = bin(byte1 ^ byte2).count('1')
                diff_bits_count += differing_bits
        
        # Check if both files reached the end
        extra_data1 = f1.read()
        extra_data2 = f2.read()
        
        if extra_data1:
            diff_bits_count += len(extra_data1) * 8
        if extra_data2:
            diff_bits_count += len(extra_data2) * 8
        
        if diff_bits_count == 0:
            print("The files are identical.")
        else:
            print(f"The files differ by {diff_bits_count} bits.")
        return diff_bits_count

# Example usage
file1 = 'data.bin'
file2 = 'extracted_data.bin'
compare_bin_files(file1, file2)
