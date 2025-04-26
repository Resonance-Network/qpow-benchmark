import matplotlib.pyplot as plt
import numpy as np
import json
from scipy.stats import expon, lognorm

# Assume times are in seconds; adjust if in milliseconds or other units
block_times = [
    a
    for a in json.load(open('./blocktimes.json', 'r'))
]
print('block_times: {}'.format(block_times))

# Convert block times to a NumPy array for easier manipulation
block_times = np.array(block_times)

# Configuration
min_time = min(block_times)  # Start of first bucket
max_time = max(block_times)  # End of last bucket

# Histogram with density normalization
bin_width = 10
bins = np.arange(0, max_time + bin_width, bin_width)
counts, bins, _ = plt.hist(block_times, bins=bins, edgecolor='black', alpha=0.7, density=True)

# Fit shifted exponential distribution (let loc be estimated)
loc, scale = expon.fit(block_times)  # loc is not fixed, allowing shift
exp_pdf = expon.pdf(bins, loc=loc, scale=scale)
plt.plot(bins, exp_pdf, 'r-', label=f'Exponential (loc={loc:.2f}, scale={scale:.2f})')

# Fit log-normal distribution
shape, loc, scale = lognorm.fit(block_times, floc=0)
lognorm_pdf = lognorm.pdf(bins, shape, loc=loc, scale=scale)
plt.plot(bins, lognorm_pdf, 'g-', label=f'Log-Normal (shape={shape:.2f})')


# Customize plot
plt.xlabel('Block Time (ms)')
plt.ylabel('Density')
plt.title('Histogram of Block Times')
plt.grid(True, alpha=0.3)

# Optional: Add median and average lines
median_time = np.median(block_times)
mean_time = np.mean(block_times)
plt.axvline(median_time, color='red', linestyle='--', label=f'Median: {median_time:.2f}s')
plt.axvline(mean_time, color='green', linestyle='--', label=f'Mean: {mean_time:.2f}s')
plt.legend()

# Print summary statistics
print(f"Number of blocks: {len(block_times)}")
print(f"Median block time: {median_time:.2f} ms")
print(f"Mean block time: {mean_time:.2f} ms")
print(f"Mean / median: {mean_time/median_time:.2f}")
print(f"Standard deviation: {np.std(block_times):.2f} ms")
print(f"Coeff of variation: {np.std(block_times)/mean_time:.2f}")


# Show plot
plt.show()

