import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def convert_and_concatenate_videos(input_folder, output_file):
    clips = []
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.3gp', '.mts', '.m2ts', '.ogv', '.vob', '.ts', '.swf', '.f4v', '.mp4')):
            input_path = os.path.join(input_folder, filename)
            
            try:
                if filename.lower().endswith('.mp4'):
                    mp4_clip = VideoFileClip(input_path)
                else:
                    video = VideoFileClip(input_path)
                    output_path = os.path.splitext(filename)[0] + ".mp4"
                    video.write_videofile(output_path, codec='libx264')
                    mp4_clip = VideoFileClip(output_path)
                    os.remove(output_path)
                
                clips.append(mp4_clip)
                print(f"Added {filename} to the combined video.")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
    
    if clips:
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_file, codec='libx264')
        print(f"Concatenated video files into {output_file}")
    else:
        print("No valid video files found to concatenate.")

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
    input_folder = r'Video_input_folder'  # Replace with your input folder path
    output_file = r'concatenated_Video.mp4'  # Replace with your desired output file path
    
    convert_and_concatenate_videos(input_folder, output_file)
    #delete_folder(input_folder)

if __name__ == "__main__":
    main()
