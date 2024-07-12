import os
from pydub import AudioSegment

def convert_and_concatenate_to_mp3(input_folder, output_file):
    combined = AudioSegment.empty()
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.wav', '.aac', '.flac', '.m4a', '.ogg', '.aiff', '.aif', '.wma', '.pcm', '.amr', '.ape')):
            input_path = os.path.join(input_folder, filename)
            
            audio = AudioSegment.from_file(input_path)
            audio_mp3 = audio.export(format="mp3")
            audio = AudioSegment.from_mp3(audio_mp3)
            combined += audio
            
            print(f"Converted and added {filename} to the combined audio.")
    
    combined.export(output_file, format="mp3")
    print(f"Concatenated audio files into {output_file}")

def delete_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                delete_folder(file_path)
        os.rmdir(folder_path)
        print(f"Deleted the folder: {folder_path}")
    except Exception as e:
        print(f"Error: {folder_path} : {e}")

def main():
    input_folder = r'Audio_input_folder'  # Replace with your input folder path
    output_file = r'concatenated_Audio.mp3'  # Replace with your desired output file path
    
    convert_and_concatenate_to_mp3(input_folder, output_file)
    delete_folder(input_folder)

if __name__ == "__main__":
    main()
