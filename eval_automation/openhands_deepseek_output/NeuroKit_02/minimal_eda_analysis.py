import csv
import math
import statistics

def process_eda(file_path):
    # Read EDA data (with null handling)
    with open(file_path) as f:
        reader = csv.DictReader(f)
        eda_values = []
        for row in reader:
            try:
                if row['EDA']:  # Skip empty values
                    eda_values.append(float(row['EDA']))
            except (ValueError, KeyError):
                continue  # Skip invalid entries
    
    # Basic analysis
    mean = statistics.mean(eda_values)
    std_dev = statistics.stdev(eda_values)
    min_val = min(eda_values)
    max_val = max(eda_values)
    
    # Simple peak detection (threshold-based)
    threshold = mean + std_dev
    peaks = [val for val in eda_values if val > threshold]
    
    # Save results
    with open('eda_results.txt', 'w') as f:
        f.write(f"EDA Analysis Results:\n")
        f.write(f"Mean: {mean:.2f} μS\n")
        f.write(f"Std Dev: {std_dev:.2f} μS\n")
        f.write(f"Min: {min_val:.2f} μS\n")
        f.write(f"Max: {max_val:.2f} μS\n")
        f.write(f"Peaks detected: {len(peaks)}\n")
    
    print("Basic EDA analysis completed. Results saved to eda_results.txt")

# Process the input file
process_eda("/data/data/agent_test_codebase/GitTaskBench/queries/NeuroKit_02/input/eda_analysis_01_input.csv")