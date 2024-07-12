import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(f"Successfully ran {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

def main():
    scripts = [
        'Convert_mp3.py',
        'get_Audio_max_Capacity.py',
        'folder_to_binary.py',
        'encrypt.py',
        'get_bin_file_Capacity.py',
        'number_seconds_needed.py',
        'Cut_Audio.py',
        'audio_encoding.py'
    ]

    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
