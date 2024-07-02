import numpy as np

def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    matrix = [list(map(int, line.strip().split())) for line in lines]
    return np.array(matrix)

def compare_matrices(file1, file2):
    matrix1 = read_matrix_from_file(file1)
    matrix2 = read_matrix_from_file(file2)

    if matrix1.shape != matrix2.shape:
        raise ValueError("Matrices must have the same dimensions to compare.")

    diff_matrix = np.abs(matrix1 - matrix2)
    max_diff = np.max(diff_matrix)

    return max_diff

# Example usage
file1 = 'stego_encoded_coefficients.txt'  # Replace with your first matrix file path
file2 = 'reconstructed_gray_image_dct.txt'  # Replace with your second matrix file path

max_diff = compare_matrices(file1, file2)
print(f"The maximum difference between corresponding values in the matrices is: {max_diff}")
