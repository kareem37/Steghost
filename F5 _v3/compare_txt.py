import numpy as np

def load_matrix_from_txt(filename):
    return np.loadtxt(filename, dtype=int)

def count_differences_between_matrices(file1, file2):
    # Load matrices from the text files
    matrix1 = load_matrix_from_txt(file1)
    matrix2 = load_matrix_from_txt(file2)
    
    # Ensure the matrices have the same shape
    if matrix1.shape != matrix2.shape:
        raise ValueError("Matrices have different shapes")
    
    # Count the number of differing values
    differences = np.sum(matrix1 != matrix2)
    
    percentage = differences / (matrix1.shape[0] * matrix1.shape[1])
    print (matrix1.shape[0] * matrix1.shape[1])
    
    return differences, percentage

# Example usage
file1 = 'stego_encoded_coefficients.txt'
file2 = 'gray_dct_coefficients.txt'
differences, percentage = count_differences_between_matrices(file1, file2)

print(f"The number of differing corresponding values between the matrices: {differences} = {percentage * 100} %")
