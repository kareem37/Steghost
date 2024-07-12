import wave
import os
from pydub import AudioSegment


def write_dimensions_to_file(output_file, total_capacity):
    # Calculate capacity in different units
    capacity_in_bytes = total_capacity / 8
    capacity_in_kilobytes = capacity_in_bytes / 1024
    capacity_in_megabytes = capacity_in_kilobytes / 1024
    capacity_in_gigabytes = capacity_in_megabytes / 1024

    # Write the capacities to the file
    with open(output_file, 'w') as file:
        file.write(f"Total Capacity: {total_capacity} bits\n")
        file.write(f"Total Capacity: {capacity_in_bytes:.2f} bytes\n")
        file.write(f"Total Capacity: {capacity_in_kilobytes:.2f} KB\n")
        file.write(f"Total Capacity: {capacity_in_megabytes:.2f} MB\n")
        file.write(f"Total Capacity: {capacity_in_gigabytes:.2f} GB\n")
        file.write(f"==============================================\n")
        
def calculate_max_capacity(audio_path, bits_per_sample):
    # Load the audio file and convert to wav
    audio = AudioSegment.from_mp3(audio_path)
    temp_wav_path = "temp.wav"
    audio.export(temp_wav_path, format="wav")
    audio_wave = wave.open(temp_wav_path, mode='rb')
    
    try:
        frame_bytes = bytearray(list(audio_wave.readframes(audio_wave.getnframes())))
        
        # Ensure the frame bytes can hold the bit string
        max_capacity_bits = len(frame_bytes) * bits_per_sample

        return max_capacity_bits
    
    finally:
        audio_wave.close()
        os.remove(temp_wav_path)

def main(Audio_path, output_file):    
    bits_per_sample = 3
    max_capacity = calculate_max_capacity(Audio_path, bits_per_sample)
    write_dimensions_to_file(output_file, max_capacity)

if __name__ == "__main__":
    Audio_path = r'audio.mp3'
    output_file = r'User_Output_Statistics\Audio_max_Capacity.txt'
    main(Audio_path, output_file)
