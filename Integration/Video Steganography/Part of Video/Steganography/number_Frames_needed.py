def read_capacity_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        capacities = {
            "LSB_4": int(lines[0].split(': ')[1].split()[0]),
            "F5": int(lines[1].split(': ')[1].split()[0]),
            "Adaptive_threshold": int(lines[2].split(': ')[1].split()[0])
        }
    return capacities

def read_total_capacity_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        total_capacity_bits = int(lines[0].split(': ')[1].split()[0])
    return total_capacity_bits

def calculate_frames_needed(total_capacity_bits, capacities):
    total_capacity_needed = total_capacity_bits
    frame_pattern = ["LSB_4", "LSB_4", "LSB_4", "F5", "F5", "Adaptive_threshold"]
    pattern_index = 0
    frames_needed = 0

    while total_capacity_needed > 0:
        current_algorithm = frame_pattern[pattern_index]
        total_capacity_needed -= capacities[current_algorithm]
        frames_needed += 1
        pattern_index = (pattern_index + 1) % len(frame_pattern)

    return frames_needed

def write_frames_needed_to_file(output_file, frames_needed):
    with open(output_file, 'w') as file:
        file.write(f"Total number of frames needed: {frames_needed}\n")

def main(algorithms_file, total_capacity_file, output_file):
    capacities = read_capacity_file(algorithms_file)
    total_capacity_bits = read_total_capacity_file(total_capacity_file)
    frames_needed = calculate_frames_needed(total_capacity_bits, capacities)
    write_frames_needed_to_file(output_file, frames_needed)
    print(f"Total number of frames needed written to {output_file}")

if __name__ == "__main__":
    algorithms_file = r'User_Output_Statistics\Algorithms_max_Capacity.txt'
    total_capacity_file = r'User_Output_Statistics\folder_data_Capacity.txt'
    output_file = r'User_Output_Statistics\frames_needed.txt'
    main(algorithms_file, total_capacity_file, output_file)
