import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python', script_name], check=True, capture_output=True, text=True)
        print(f"Successfully ran {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

def main():
    scripts = [
        'get_Image_max_Capacity.py',
        'folder_to_binary.py',
        'encrypt.py',
        'get_bin_file_Capacity.py',
        'run_Steganography.py'
    ]

    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()
