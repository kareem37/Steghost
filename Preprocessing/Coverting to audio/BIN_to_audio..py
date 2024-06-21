import wave
import struct

def binary_to_wav(binary_file_path, wav_file_path, sample_rate=44100, sample_width=2, channels=1):
    """
    Convert a binary file to a WAV sound file.
    
    :param binary_file_path: Path to the input binary file
    :param wav_file_path: Path to the output WAV file
    :param sample_rate: Sample rate of the audio (default: 44100)
    :param sample_width: Sample width in bytes (default: 2, which is 16-bit audio)
    :param channels: Number of audio channels (default: 1, which is mono)
    """
    with open(binary_file_path, 'rb') as bin_file:
        binary_data = bin_file.read()
    
    # Create a wave write object
    with wave.open(wav_file_path, 'w') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        
        # Interpret the binary data as PCM samples
        if sample_width == 1:
            # 8-bit audio, unsigned
            fmt = f'{len(binary_data)}B'
            pcm_data = struct.unpack(fmt, binary_data)
            wav_data = struct.pack(fmt, *pcm_data)
        elif sample_width == 2:
            # 16-bit audio, signed
            fmt = f'{len(binary_data) // 2}h'
            pcm_data = struct.unpack(fmt, binary_data)
            wav_data = struct.pack(fmt, *pcm_data)
        else:
            raise ValueError("Unsupported sample width")
        
        # Write the PCM data to the WAV file
        wav_file.writeframes(wav_data)

# Example usage
if __name__ == "__main__":
    binary_to_wav('D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output_binary_file.bin', 'D:\Study -2\Y4 S2\GP\Coding\SteGhost\Preprocessing\Convering\output_sound_file.wav')
