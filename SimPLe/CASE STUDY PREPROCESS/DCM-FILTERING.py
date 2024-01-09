import pandas as pd
import os
import shutil

# Function to extract slice number from file name
def extract_slice_number(filename):
    # This function needs to be customized to extract the actual slice number from your filenames
    print("Processing file:", filename)
    # The logic here will depend on the naming convention of the DICOM files
    # Example: 'slice_00123.dcm' -> 123
    slice_part = filename.split('-')[-1].split('.')[0]  # Adjust according to your file naming convention
    try:
        return int(slice_part)  # Strip leading zeroes and convert to integer
    except ValueError:
        print("Could not extract slice number from:", filename)
        return None

# Load the annotation data
annotations_df = pd.read_excel("Annotation_Boxes.xlsx")

# Base directory where all the patient directories are stored
base_dicom_dir = 'Duke-Breast-Cancer-MRI'  # Update this path to the location of your DICOM files

# Directory to store the selected DICOM files
output_dir = 'DCM-NII-SLICED'
os.makedirs(output_dir, exist_ok=True)

# Process each patient
for index, row in annotations_df.iterrows():
    patient_id = row['Patient ID']
    start_slice = row['Start Slice']
    end_slice = row['End Slice']
    print("Processing patient:", patient_id)

    # Path for the current patient
    patient_base_dir = os.path.join(base_dicom_dir, patient_id)

    # Check if the patient directory exists
    if not os.path.isdir(patient_base_dir):
        print(f"Directory not found for patient {patient_id}, skipping.")
        continue

    # Iterate through all subdirectories for the patient
    for date_dir in os.listdir(patient_base_dir):
        date_path = os.path.join(patient_base_dir, date_dir)
        # Check if it's a directory
        if os.path.isdir(date_path):
            # Now iterate through all sequence directories inside this date directory
            for sequence_dir in os.listdir(date_path):
                sequence_path = os.path.join(date_path, sequence_dir)
                if os.path.isdir(sequence_path):
                    print("Processing sequence:", sequence_dir)
                    # Create output directory for this sequence
                    sequence_output_dir = os.path.join(output_dir, patient_id, date_dir, sequence_dir)
                    os.makedirs(sequence_output_dir, exist_ok=True)

                    # Copy relevant slices for this sequence
                    for file in os.listdir(sequence_path):
                        if file.endswith('.dcm'):
                            slice_number = extract_slice_number(file)
                            if slice_number is not None and start_slice <= slice_number <= end_slice:
                                src_file = os.path.join(sequence_path, file)
                                dest_file = os.path.join(sequence_output_dir, file)
                                shutil.copy2(src_file, dest_file)
                                print(f"Copied slice {slice_number} for patient {patient_id} from {sequence_dir}")

print("DICOM files copied successfully.")
