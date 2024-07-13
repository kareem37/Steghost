
import sys
from pydub import AudioSegment
import wave
import os

def hide_data_in_audio(cover_audio_path, bin_data_path, stego_audio_wav_path, stego_audio_mp3_path, bits_per_sample=3):
    # Load the cover audio and convert it to wav
    audio = AudioSegment.from_mp3(cover_audio_path)
    temp_wav_path = "temp.wav"
    audio.export(temp_wav_path, format="wav")
    audio_wave = wave.open(temp_wav_path, mode='rb')
    
    try:
        with open(bin_data_path, "rb") as f:
            data = f.read()
        
        # Convert data to a bit string
        bits = ''.join([format(byte, '08b') for byte in data])
        robust_marker = '1111111100000000'  # More unique padding to indicate end of data
        bits += robust_marker

        frame_bytes = bytearray(list(audio_wave.readframes(audio_wave.getnframes())))

        # Ensure the frame bytes can hold the bit string
        available_bits = len(frame_bytes) * bits_per_sample
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
        
        # Convert the stego wav file to mp3
        stego_audio = AudioSegment.from_wav(stego_audio_wav_path)
        stego_audio.export(stego_audio_mp3_path, format="mp3")
    finally:
        audio_wave.close()
        os.remove(temp_wav_path)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python encode.py <cover_audio_path> <bin_data_path> <stego_audio_wav_path> <stego_audio_mp3_path> <bits_per_sample>")
        sys.exit(1)

    cover_audio_path = sys.argv[1]
    bin_data_path = sys.argv[2]
    stego_audio_wav_path = sys.argv[3]
    stego_audio_mp3_path = sys.argv[4]
    bits_per_sample = int(sys.argv[5])

    hide_data_in_audio(cover_audio_path, bin_data_path, stego_audio_wav_path, stego_audio_mp3_path, bits_per_sample)
