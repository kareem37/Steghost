import os
from pydub import AudioSegment

def read_needed_duration(file_path):
    with open(file_path, 'r') as file:
        line = file.readline().strip()
        needed_duration_seconds = float(line.split(":")[1].strip().split()[0])
    return needed_duration_seconds

def convert_and_cut_audio(input_mp3_path, output_wav_path, needed_duration_seconds):
    # Convert MP3 to WAV
    audio = AudioSegment.from_mp3(input_mp3_path)
    
    # Cut the audio to the needed duration
    cut_audio = audio[:needed_duration_seconds * 1000]  # Convert seconds to milliseconds
    
    # Export the cut audio as WAV
    cut_audio.export(output_wav_path, format="wav")

def main():
    needed_duration_file = r'User_Output_Statistics\seconds_needed.txt'
    input_mp3_path = r'audio.mp3'
    output_wav_path = r'audio.wav'
    
    # Read the needed duration from the file
    needed_duration_seconds = read_needed_duration(needed_duration_file)
    
    if needed_duration_seconds == -1:
        print("Data capacity exceeds audio capacity. No action taken.")
    else:
        # Convert and cut the audio
        convert_and_cut_audio(input_mp3_path, output_wav_path, needed_duration_seconds)
        print(f"Audio has been converted and cut to {needed_duration_seconds:.2f} seconds.")
    
    # Delete the input MP3 file
    try:
        os.remove(input_mp3_path)
        print(f"Deleted the input MP3 file: {input_mp3_path}")
    except OSError as e:
        print(f"Error: {input_mp3_path} : {e.strerror}")

if __name__ == "__main__":
    main()
