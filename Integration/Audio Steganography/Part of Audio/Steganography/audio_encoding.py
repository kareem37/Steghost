import sys
from pydub import AudioSegment
import wave
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

def convert_mp3_to_wav(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    wav_path = mp3_path.replace('.mp3', '.wav')
    audio.export(wav_path, format="wav")
    return wav_path

def hide_data_in_audio(cover_audio_path, bin_data_path, stego_audio_wav_path, bits_per_sample=3):
    # Convert MP3 to WAV if necessary
    if cover_audio_path.endswith('.mp3'):
        cover_audio_path = convert_mp3_to_wav(cover_audio_path)
    
    # Load the cover audio directly as wav
    audio_wave = wave.open(cover_audio_path, mode='rb')
    
    try:
        with open(bin_data_path, "rb") as f:
            data = f.read()
        
        # Calculate the length of the binary data
        data_length = len(data)
        # Convert the length to a 30-bit binary representation
        length_bits = format(data_length, '030b')
        print(f"Length of binary file: {data_length}")
        print(f"Binary representation (30 bits): {length_bits}")
        
        # Convert data to a bit string
        bits = ''.join([format(byte, '08b') for byte in data])
        
        # Prepend the 30-bit length to the data bits
        bits = length_bits + bits
        
        robust_marker = '11111111000000001111111100000000'  # More unique padding to indicate end of data
        bits += robust_marker

        frame_bytes = bytearray(list(audio_wave.readframes(audio_wave.getnframes())))
        
        # Ensure the frame bytes can hold the bit string
        available_bits = len(frame_bytes) * bits_per_sample
        print("Available bits Can Hide: ", available_bits)
        print("Available Data: ", len(bits))
        if len(bits) > available_bits:
            raise ValueError("Data is too large to hide in cover audio.")

        # Modify the least significant bits of each byte in the audio frame bytes
        bit_index = 0
        for i in range(len(frame_bytes)):
            for j in range(bits_per_sample):
                if bit_index < len(bits):
                    frame_bytes[i] = (frame_bytes[i] & ~(1 << j)) | (int(bits[bit_index]) << j)
                    bit_index += 1

        modified_frames = bytes(frame_bytes)
        with wave.open(stego_audio_wav_path, 'wb') as fd:
            fd.setparams(audio_wave.getparams())
            fd.writeframes(modified_frames)
        
    finally:
        audio_wave.close()
        if cover_audio_path.endswith('.wav'):
            os.remove(cover_audio_path)  # Clean up the temporary WAV file

if __name__ == "__main__":
    cover_audio_path = r'audio.wav'
    bin_data_path = r'encrypted_data.bin'
    stego_audio_wav_path = r'User_output\stego_audio.wav'
    bits_per_sample = 3

    hide_data_in_audio(cover_audio_path, bin_data_path, stego_audio_wav_path, bits_per_sample)
    # Delete bin file
    delete_bin_file(bin_data_path)
    # Delete the input cover_audio file
    try:
        os.remove(cover_audio_path)
        print(f"Deleted the input Wav file: {cover_audio_path}")
    except OSError as e:
        print(f"Error: {cover_audio_path} : {e.strerror}")
