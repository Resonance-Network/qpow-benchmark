# QPoW Benchmark

This repository contains a benchmark tool for the QPoW (Quantum Proof of Work) algorithm implementation found in the `qpow-math` crate. It measures the time and number of nonce attempts required to find a valid PoW solution for various difficulty levels. It also includes a Python script to visualize the results.

## Prerequisites

*   **Rust:** Ensure you have Rust installed. You can get it from [rustup.rs](https://rustup.rs/).
*   **Python 3:** Ensure you have Python 3 installed. You can get it from [python.org](https://www.python.org/).

## Access

This repository refers to a private repository on gitlab, you need to (A) have access, and (B) set up your access, either SSH key or PAT.

## Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone git@github.com:Resonance-Network/qpow-benchmark.git
    cd qpow-benchmark
    ```

2.  **Set up Python virtual environment:**
    ```bash
    # Create the virtual environment (only needs to be done once)
    python3 -m venv .venv

    # Activate the virtual environment (needs to be done in each new terminal session)
    # On macOS/Linux (bash/zsh):
    source .venv/bin/activate
    # On Windows (cmd.exe):
    # .venv\Scripts\activate.bat
    # On Windows (PowerShell):
    # .venv\Scripts\Activate.ps1

    # Install required Python packages
    pip install pandas matplotlib numpy
    ```

## Running the Benchmark

To run the benchmark directly and see the output in the console:

```bash
# Compile and run in release mode for accurate timing
cargo run --release
```

## Generating Plots

To visualize the benchmark results:

1.  **Run the benchmark and save the output to a file:**
    ```bash
    cargo run --release > nonce_data.txt
    ```
    This will execute the benchmark and redirect the standard output (which contains the results per difficulty level) into a file named `nonce_data.txt`.

2.  **Run the Python plotting script:**
    Make sure your Python virtual environment is activated (`source .venv/bin/activate`).
    ```bash
    python plot_nonces.py nonce_data.txt
    ```
    This will read `nonce_data.txt`, process the data, display a plot on the screen, and save the plot as `difficulty_vs_metrics.png`.

    You can optionally provide a different input filename:
    ```bash
    python plot_nonces.py your_output_file.txt
    ```

## Understanding the Output

The benchmark outputs lines in the following format for each difficulty tested:

```
Difficulty: <difficulty_value>, Average Nonce Count: <avg_nonces>, Avg Time: <avg_time> s, Aggregate Hash Rate: <hash_rate> (solutions/s)
```

The Python script generates a plot showing:
*   Average Nonce Count vs. Difficulty
*   Average Time per Solution vs. Difficulty
*   The overall average hash rate calculated across all successful samples.
*   The detected CPU information in the plot title.
