import hashlib
import numpy as np
from scipy.stats import chisquare
from math import gcd
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

# Simulate U512 and U256 as Python integers (since Python has arbitrary-precision integers)
def u512_from_bytes(bytes):
    return int.from_bytes(bytes, byteorder='big')

def u512_to_bytes(value, num_bytes=64):
    return value.to_bytes(num_bytes, byteorder='big')

# Reimplement hash_to_group in Python
def hash_to_group(h, m, n, s):
    # Ensure m is coprime to n (required for exponentiation in Z_n^*)
    if gcd(m, n) != 1:
        # In practice, this is extremely unlikely with SHA hashes
        # For testing, we can adjust m to be coprime
        m = m + 1 if m % 2 == 0 else m - 1  # Simple adjustment (assumes n is odd)

    h_int = u512_from_bytes(h)
    h_plus_s = (h_int + s) % (2**512)  # Simulate U512 addition
    # Exponentiation: m^(h + s) mod n
    return pow(m, h_plus_s, n)

# Reimplement reverse_bytes in Python
def reverse_bytes(value):
    bytes = u512_to_bytes(value)
    reversed_bytes = bytes[::-1]
    return u512_from_bytes(reversed_bytes)

def reverse_bits(value):
    binary = bin(value)[2:].zfill(512)  # Ensure 512 bits
    reversed_binary = binary[::-1]
    return int(reversed_binary, 2)

# Generate a random permutation based on the header h
def generate_byte_permutation(h):
    seed = int.from_bytes(hashlib.sha256(h).digest(), byteorder='big')
    indices = list(range(64))  # 64 bytes (512 bits)
    random.seed(seed)
    random.shuffle(indices)
    return indices

def apply_byte_permutation(value, permutation):
    bytes = u512_to_bytes(value)  # 64 bytes
    permuted_bytes = [0] * 64
    for i in range(64):
        permuted_bytes[permutation[i]] = bytes[i]
    return u512_from_bytes(permuted_bytes)

# Generate inputs for testing
def generate_inputs():
    # Simulate a block header (as a 512-bit integer)
    header = bytes([random.randint(0, 255) for _ in range(64)])  # 64 random bytes (512 bits)

    m = u512_from_bytes(hashlib.sha256(header).digest())
    n = u512_from_bytes(hashlib.sha512(header).digest())

    return header, m, n

# Test uniformity of hash_to_group outputs
def test_uniformity(num_samples=100000, num_bins=100):

    # Generate outputs by varying the nonce s
    outputs_before = []
    outputs_after = []
    for _ in tqdm(range(num_samples)):
        h, m, n = generate_inputs()
        s = random.randint(1, n)
        # Raw output of hash_to_group
        result = hash_to_group(h, m, n, s)
        outputs_before.append(result)

        # Output after permutation
#         permutation = generate_byte_permutation(h)
#         result_permuted = apply_byte_permutation(result, permutation)
#         result = reverse_bytes(result)
        result_hashed = u512_from_bytes(hashlib.sha512(u512_to_bytes(result)).digest())
        outputs_after.append(result_hashed)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))


    print("Testing uniformity before permutation (modulo n)...")
    test_distribution(outputs_before, num_bins, modulus=2**512, ax_hist=ax1, ax_fft=ax3, title="Before permutation")

    print("\nTesting uniformity after permutation (in Z_2^512)...")
    test_distribution(outputs_after, num_bins, modulus=2**512, ax_hist=ax2, ax_fft=ax4, title="After permutation")

    plt.tight_layout()
    plt.show()

def test_distribution(outputs, num_bins, modulus, ax_hist, ax_fft, title):
    # Bin the outputs
    # Scale outputs to [0, num_bins) by mapping [0, modulus) to [0, num_bins)
    bins = np.zeros(num_bins, dtype=np.int64)
    for output in outputs:
        # Map output to a bin: (output / modulus) * num_bins
        bin_index = int((output * num_bins) // modulus)
        bins[bin_index] += 1

    # Expected frequency under uniform distribution
    expected_freq = len(outputs) / num_bins

    # Perform Chi-Square test
    observed = bins
    expected = np.full(num_bins, expected_freq)
    chi_square_stat, p_value = chisquare(observed, expected)

    print(f"Chi-Square Statistic: {chi_square_stat:.2f}")
    print(f"P-Value: {p_value:.4f}")
    print("Interpretation:")
    if p_value < 0.05:
        print("  - Distribution is NOT uniform (p-value < 0.05)")
    else:
        print("  - Distribution appears uniform (p-value >= 0.05)")

    # Plot the histogram
    ax_hist.bar(range(num_bins), bins, alpha=0.7, label='Observed Frequencies', color='blue')
    ax_hist.axhline(y=expected_freq, color='red', linestyle='--', label=f'Expected Uniform Frequency ({expected_freq:.1f})')
    ax_hist.set_xlabel('Bin Index')
    ax_hist.set_ylabel('Frequency')
    ax_hist.set_title(title)
    ax_hist.legend()
    ax_hist.grid(True, alpha=0.3)

    # Compute FFT of the binned frequencies
    fft_result = np.fft.fft(bins - expected_freq)  # Subtract mean to center the signal
    fft_magnitude = np.abs(fft_result)[:num_bins//2]  # Take magnitude, first half (positive frequencies)
    frequencies = np.fft.fftfreq(num_bins)[:num_bins//2]  # Corresponding frequencies

    # Plot the FFT spectrum
    ax_fft.plot(frequencies, fft_magnitude, label='FFT Magnitude', color='purple')
    ax_fft.set_xlabel('Frequency')
    ax_fft.set_ylabel('Magnitude')
    ax_fft.set_title(f'FFT of {title}')
    ax_fft.legend()
    ax_fft.grid(True, alpha=0.3)



# Run the test
if __name__ == "__main__":
    test_uniformity(num_samples=10000, num_bins=100)