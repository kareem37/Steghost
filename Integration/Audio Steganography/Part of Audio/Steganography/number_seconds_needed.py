import os
from pydub import AudioSegment
import wave
import math


def read_capacity(file_path):
    capacities = {}
    with open(file_path, 'r') as file:
        for line in file:
            if "bits" in line:
                capacities['bits'] = float(line.split(":")[1].strip().split()[0])
            elif "bytes" in line:
                capacities['bytes'] = float(line.split(":")[1].strip().split()[0])
            elif "KB" in line:
                capacities['KB'] = float(line.split(":")[1].strip().split()[0])
            elif "MB" in line:
                capacities['MB'] = float(line.split(":")[1].strip().split()[0])
            elif "GB" in line:
                capacities['GB'] = float(line.split(":")[1].strip().split()[0])
    return capacities

def calculate_needed_duration(audio_path, data_capacity_bits, bits_per_sample):
    # Load the audio file and convert to wav
    audio = AudioSegment.from_mp3(audio_path)
    temp_wav_path = "temp.wav"
    audio.export(temp_wav_path, format="wav")
    audio_wave = wave.open(temp_wav_path, mode='rb')
    
    try:       
        # Get audio parameters
        n_channels = audio_wave.getnchannels()
        frame_rate = audio_wave.getframerate()
       
        # Calculate number of audio n_frames needed
        frame_bytes_count = data_capacity_bits / bits_per_sample
        n_frames = frame_bytes_count * n_channels / 8
                
        # Calculate duration needed in seconds
        duration_needed = math.ceil(n_frames / frame_rate)
        
        return duration_needed
    
    finally:
        audio_wave.close()
        os.remove(temp_wav_path)

def main(algorithm_total_capacity_file, data_total_capacity_file, cover_audio_path ,output_file):
    # Read capacities from the files
    algorithm_capacity = read_capacity(algorithm_total_capacity_file)
    data_capacity = read_capacity(data_total_capacity_file)
    
    # Extract the bit capacities
    data_capacity_bits = data_capacity['bits']
    algorithm_capacity_bits = algorithm_capacity['bits']
    
    # Check if data capacity is greater than algorithm capacity
    if data_capacity_bits > algorithm_capacity_bits:
        needed_duration_seconds = -1
    else:
        # Use the first audio file to calculate the needed duration
        
        bits_per_sample = 3

        # Calculate the needed duration to hide the data
        needed_duration_seconds = calculate_needed_duration(cover_audio_path, data_capacity_bits, bits_per_sample)

    # Write the result to the output file
    with open(output_file, 'w') as file:
        if needed_duration_seconds == -1:
            file.write("Needed duration to embed the data: -1 (Data capacity exceeds audio capacity)\n")
        else:
            file.write(f"Needed duration to embed the data: {needed_duration_seconds:.2f} seconds\n")

if __name__ == "__main__":
    algorithm_total_capacity_file = r'User_Output_Statistics\Audio_max_Capacity.txt'
    data_total_capacity_file = r'User_Output_Statistics\folder_data_Capacity.txt'
    output_file = r'User_Output_Statistics\seconds_needed.txt'
    cover_audio_path = r'audio.mp3'
    main(algorithm_total_capacity_file, data_total_capacity_file, cover_audio_path, output_file)
