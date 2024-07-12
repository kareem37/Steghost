import sys
import wave
import os

def extract_data_from_audio(stego_audio_path, output_bin_path, bits_per_sample=3):
    audio_wave = wave.open(stego_audio_path, mode='rb')
    
    try:
        frame_bytes = bytearray(list(audio_wave.readframes(audio_wave.getnframes())))
        
        # Extract the least significant bits
        extracted_bits = []
        for byte in frame_bytes:
            for j in range(bits_per_sample):
                extracted_bits.append(str((byte >> j) & 1))
        
        extracted_bits = ''.join(extracted_bits)

        # Extract the first 30 bits to get the length of the binary data
        length_bits = extracted_bits[:30]
        data_length = int(length_bits, 2)
        print(f"Extracted binary length (30 bits): {length_bits}")
        print(f"Length of binary file: {data_length}")

        # Extract the binary data using the data length
        data_bits = extracted_bits[30:30 + data_length * 8]

        # Find the position of the end marker (1111111100000000)
        robust_marker = '11111111000000001111111100000000'
        end_index = data_bits.find(robust_marker)
        print(f"End marker found at bit index: {end_index}")
        if end_index != -1:
            data_bits = data_bits[:end_index]

        # Log the length of the extracted bits
        print(f"Length of extracted bits: {len(data_bits)}")

        # Convert the extracted bit string back to bytes
        byte_array = bytearray()
        for i in range(0, len(data_bits), 8):
            byte = data_bits[i:i+8]
            if len(byte) == 8:
                byte_array.append(int(byte, 2))

        with open(output_bin_path, "wb") as f:
            f.write(byte_array)
    finally:
        audio_wave.close()



if __name__ == "__main__":
    
    stego_audio_path = r'User_Input\stego_audio.wav'
    output_bin_path = 'extracted_folder_data.bin'
    bits_per_sample = 3

    extract_data_from_audio(stego_audio_path, output_bin_path, bits_per_sample)