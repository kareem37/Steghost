from numba import cuda
import numpy as np
import time

# GPU kernel to permute pixels
@cuda.jit
def permute_pixels_gpu(channel_pixels, permuted_pixels, permuted_indices):
    idx = cuda.grid(1)
    if idx < permuted_pixels.size:
        permuted_pixels[idx] = channel_pixels[permuted_indices[idx]]

# Function to permute pixels using GPU
def permute_pixels(channel_pixels, key, Stego_Time_file):
    """Permute pixels using a given key."""
    start_time = time.time()
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(channel_pixels))
    print('GPU: permuted_indices: ', permuted_indices )  
    permuted_pixels = np.zeros_like(channel_pixels)
    
    d_channel_pixels = cuda.to_device(channel_pixels)
    d_permuted_pixels = cuda.device_array_like(permuted_pixels)
    d_permuted_indices = cuda.to_device(permuted_indices)

    threads_per_block = 256
    blocks_per_grid = (len(channel_pixels) + (threads_per_block - 1)) // threads_per_block
    
    permute_pixels_gpu[blocks_per_grid, threads_per_block](d_channel_pixels, d_permuted_pixels, d_permuted_indices)
    permuted_pixels = d_permuted_pixels.copy_to_host()
    print('GPU: permuted_pixels: ', permuted_pixels )  
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"permute_pixels execution time: {execution_time:.6f} seconds", Stego_Time_file)
    
    
    return permuted_pixels, permuted_indices, execution_time

# GPU kernel to reverse permute pixels
@cuda.jit
def reverse_permute_pixels_gpu(permuted_pixels, original_pixels, inverse_permutation):
    idx = cuda.grid(1)
    if idx < original_pixels.size:
        original_pixels[idx] = permuted_pixels[inverse_permutation[idx]]


# Function to reverse permute pixels using GPU
def reverse_permute_pixels(permuted_pixels, permuted_indices, Stego_Time_file):
    """Reverse the permutation of pixels."""
    start_time = time.time()
    original_pixels = np.zeros_like(permuted_pixels)
    inverse_permutation = np.argsort(permuted_indices)
    print("GPU: inverse_permutation:", inverse_permutation)
    
    d_permuted_pixels = cuda.to_device(permuted_pixels)
    d_original_pixels = cuda.device_array_like(original_pixels)
    d_inverse_permutation = cuda.to_device(inverse_permutation)

    threads_per_block = 256
    blocks_per_grid = (len(permuted_pixels) + (threads_per_block - 1)) // threads_per_block
    
    reverse_permute_pixels_gpu[blocks_per_grid, threads_per_block](d_permuted_pixels, d_original_pixels, d_inverse_permutation)
    original_pixels = d_original_pixels.copy_to_host()
    print("GPU: original_pixels:", original_pixels)
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"reverse_permute_pixels execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return original_pixels, execution_time

def log_time_complexity(message, Stego_Time_file):
    with open(Stego_Time_file, 'a') as f:
        f.write(message + '\n')

def permute_pixels_cpu(channel_pixels, key, Stego_Time_file):
    """Permute pixels using a given key."""
    start_time = time.time()
    np.random.seed(key)
    permuted_indices = np.random.permutation(len(channel_pixels))
    print('CPU: permuted_indices: ', permuted_indices )  
    permuted_pixels = channel_pixels[permuted_indices]
    print('CPU: permuted_pixels: ', permuted_pixels )  
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"permute_pixels execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return permuted_pixels, permuted_indices, execution_time

def reverse_permute_pixels_cpu(permuted_pixels, permuted_indices, Stego_Time_file):
    """Reverse the permutation of pixels."""
    start_time = time.time()
    original_pixels = np.zeros_like(permuted_pixels)
    inverse_permutation = np.argsort(permuted_indices)
    print("CPU: inverse_permutation:", inverse_permutation)
    original_pixels = permuted_pixels[inverse_permutation]
    print("CPU: original_pixels:", original_pixels)
    end_time = time.time()
    execution_time = end_time - start_time
    log_time_complexity(f"reverse_permute_pixels execution time: {execution_time:.6f} seconds", Stego_Time_file)
    return original_pixels, execution_time

def compare_cpu_gpu():
    channel_pixels = np.random.randint(0, 256, size=1024).astype(np.uint8)
    print("channel_pixels: ", channel_pixels)
    key = 123
    Stego_Time_file = 'Stego_Time.txt'

    # CPU version
    permuted_pixels_cpu, permuted_indices_cpu, cpu_time = permute_pixels_cpu(channel_pixels, key, Stego_Time_file)
    original_pixels_cpu, reverse_cpu_time = reverse_permute_pixels_cpu(permuted_pixels_cpu, permuted_indices_cpu, Stego_Time_file)

    # GPU version
    permuted_pixels_gpu, permuted_indices_gpu, gpu_time = permute_pixels(channel_pixels, key, Stego_Time_file)
    original_pixels_gpu, reverse_gpu_time = reverse_permute_pixels(permuted_pixels_gpu, permuted_indices_gpu, Stego_Time_file)

    # Compare results
    assert np.array_equal(permuted_pixels_cpu, permuted_pixels_gpu), "Permuted pixels do not match!"
    assert np.array_equal(permuted_indices_cpu, permuted_indices_gpu), "Permuted indices do not match!"
    assert np.array_equal(original_pixels_cpu, original_pixels_gpu), "Original pixels do not match!"

    print(f"CPU permute time: {cpu_time:.6f} seconds")
    print(f"GPU permute time: {gpu_time:.6f} seconds")
    print(f"CPU reverse permute time: {reverse_cpu_time:.6f} seconds")
    print(f"GPU reverse permute time: {reverse_gpu_time:.6f} seconds")

if __name__ == "__main__":
    compare_cpu_gpu()
