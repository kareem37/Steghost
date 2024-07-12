import argparse
import os
from pydub import AudioSegment

# Function to convert audio file to MP3
def convert_to_mp3(input_file, output_file):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)
    
    # Export as MP3
    audio.export(output_file, format="mp3")

def main():
    # Set up argument parser
    input_folder = 'User_Cover_Audio'
    output_file = 'audio.mp3'

    # Supported audio formats
    supported_formats = ['.wav', '.aac', '.flac', '.m4a', '.ogg', '.aiff', '.aif', '.wma', '.pcm', '.amr', '.ape']

    # Convert each supported audio file in the input folder to MP3
    for filename in os.listdir(input_folder):
        if any(filename.lower().endswith(ext) for ext in supported_formats):
            input_file = os.path.join(input_folder, filename)
            convert_to_mp3(input_file, output_file)
            print(f"Converted {filename} to {output_file}")

if __name__ == "__main__":
    main()
