def write_dimensions_to_file(output_file, total_capacity):
    # Calculate capacity in different units
    capacity_in_bytes = total_capacity / 8
    capacity_in_kilobytes = capacity_in_bytes / 1024
    capacity_in_megabytes = capacity_in_kilobytes / 1024
    capacity_in_gigabytes = capacity_in_megabytes / 1024
    # Write the capacities to the file
    with open(output_file, 'w') as file:
        file.write(f"Total Capacity: {total_capacity} bits\n")
        file.write(f"Total Capacity: {capacity_in_bytes:.2f} bytes\n")
        file.write(f"Total Capacity: {capacity_in_kilobytes:.2f} KB\n")
        file.write(f"Total Capacity: {capacity_in_megabytes:.2f} MB\n")
        file.write(f"Total Capacity: {capacity_in_gigabytes:.2f} GB\n")
        
def read_binary_file(binary_file_path):
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data


def main(binary_file_path, capacities_file_path):
    binary_data_in_bytes = read_binary_file(binary_file_path)
    total_capacity = len(binary_data_in_bytes) * 8
    write_dimensions_to_file(capacities_file_path,total_capacity)


# Example usage:
binary_file_path = r'encrypted_data.bin'
capacities_file_path = r'User_Output_Statistics\folder_data_Capacity.txt'

main(binary_file_path, capacities_file_path)