
import sys
import wave

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

        # Find the position of the end marker (1111111100000000)
        robust_marker = '1111111100000000'
        end_index = extracted_bits.find(robust_marker)
        print(f"End marker found at bit index: {end_index}")
        if end_index != -1:
            extracted_bits = extracted_bits[:end_index]

        # Log the length of the extracted bits
        print(f"Length of extracted bits: {len(extracted_bits)}")

        # Convert the extracted bit string back to bytes
        byte_array = bytearray()
        for i in range(0, len(extracted_bits), 8):
            byte = extracted_bits[i:i+8]
            if len(byte) == 8:
                byte_array.append(int(byte, 2))

        with open(output_bin_path, "wb") as f:
            f.write(byte_array)
    finally:
        audio_wave.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python decode.py <stego_audio_path> <output_bin_path> <bits_per_sample>")
        sys.exit(1)

    stego_audio_path = sys.argv[1]
    output_bin_path = sys.argv[2]
    bits_per_sample = int(sys.argv[3])

    extract_data_from_audio(stego_audio_path, output_bin_path, bits_per_sample)
