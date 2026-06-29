"""
Biomedical Data Analysis Tool
Author: Apostolou Alexios
Description: A simple script to parse, clean, and analyze biomedical patient data.
"""

import os


def load_and_clean_data(filepath):
    """Reads a CSV file, skips corrupt rows, and returns a list of dictionaries."""
    parsed_patients = []

    if not os.path.exists(filepath):
        print(f"Error: The file {filepath} does not exist.")
        return []

    with open(filepath, "r") as file:
        # Read the header row
        header = file.readline().strip().split(",")

        # Process each line
        for line in file:
            values = line.strip().split(",")

            # Check for missing values (NA) in the row
            if "NA" in values:
                # Skip rows with missing critical data (Data Cleaning)
                continue

            # Parse values into a dictionary with correct data types
            try:
                patient = {
                    "PatientID": values[0],
                    "Age": int(values[1]),
                    "Gender": values[2],
                    "HeartRate": int(values[3]),
                    "SystolicBP": int(values[4]),
                    "Cholesterol": int(values[5]),
                }
                parsed_patients.append(patient)
            except ValueError:
                # Skip if there's a conversion error
                continue

    return parsed_patients


def calculate_metrics(patients):
    """Calculates basic health metrics and averages from the dataset."""
    if not patients:
        return None

    total_patients = len(patients)
    total_age = 0
    total_heart_rate = 0
    high_bp_count = 0  # Patients with Systolic BP >= 130 (Hypertension stage 1)

    for p in patients:
        total_age += p["Age"]
        total_heart_rate += p["HeartRate"]
        if p["SystolicBP"] >= 130:
            high_bp_count += 1

    metrics = {
        "Total Analyzed": total_patients,
        "Average Age": round(total_age / total_patients, 1),
        "Average Heart Rate": round(total_heart_rate / total_patients, 1),
        "Hypertension Risk Ratio (%)": round(
            (high_bp_count / total_patients) * 100, 1
        ),
    }
    return metrics


def main():
    filename = "patients_data.csv"
    
    # --- ΑΥΤΟΜΑΤΟ PATH ---
    # Βρίσκει τον φάκελο στον οποίο βρίσκεται το analyzer.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Ενώνει τον φάκελο με το όνομα του αρχείου .csv
    full_path = os.path.join(current_dir, filename)
    # ---------------------

    print("--- Biomedical Data Analyzer ---")
    print(f"Loading data from: {full_path}...")

    # 1. Load and Clean (Τώρα του περνάμε το full_path)
    cleaned_data = load_and_clean_data(full_path)

    # 2. Analyze
    results = calculate_metrics(cleaned_data)

    # 3. Present Results
    if results:
        print("\n[Analysis Successful]")
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print("\nNo valid data found to analyze.")


if __name__ == "__main__":
    main()