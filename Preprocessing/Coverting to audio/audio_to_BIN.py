import wave
import struct

def wav_to_binary(wav_file_path, binary_file_path):
    """
    Convert a WAV sound file back to a binary file.
    
    :param wav_file_path: Path to the input WAV file
    :param binary_file_path: Path to the output binary file
    """
    with wave.open(wav_file_path, 'r') as wav_file:
        params = wav_file.getparams()
        n_channels, sampwidth, framerate, n_frames = params[:4]

        frames = wav_file.readframes(n_frames)
        
        # Write the frames to the binary file
        with open(binary_file_path, 'wb') as bin_file:
            bin_file.write(frames)

# Example usage
if __name__ == "__main__":
    wav_to_binary('D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output_sound_file.wav', 'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output_binary_file.bin')
