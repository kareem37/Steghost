import os

def get_bin_file_paths(folder):
    return [os.path.join(folder, fname) for fname in os.listdir(folder) if fname.endswith('.bin')]

def combine_bin_files(folder, output_file):
    bin_file_paths = get_bin_file_paths(folder)
    bin_file_paths.sort()

    with open(output_file, 'wb') as output:
        for file_path in bin_file_paths:
            with open(file_path, 'rb') as f:
                while (chunk := f.read(1024)):  # Reading in chunks to handle large files
                    output.write(chunk)

if __name__ == "__main__":
    folder = r"input_frames_folder_data"
    output_file = r"test\combined_file.bin"
    combine_bin_files(folder, output_file)
