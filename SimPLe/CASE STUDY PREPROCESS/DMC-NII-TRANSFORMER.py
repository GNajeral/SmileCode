import os
import subprocess

# Base directory where all the patient directories are stored
base_dicom_dir = 'DCM-NII-SLICED'  # Update this path to the location of your DICOM files


# Function to call dcm2niix for conversion
def convert_dicom_to_nifti(sequence_path):
    # Convert the DICOM files in the sequence directory to compressed NIfTI format
    # The '-z y' option enables compression
    # The '-o' option specifies the output directory for the NIfTI files
    # The '-f' option specifies the filename format; %p will use the protocol name
    result = subprocess.run(['dcm2niix', '-z', 'y', '-o', sequence_path, '-f', '%p', sequence_path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result


# Iterate over each patient directory
for patient_dir in os.listdir(base_dicom_dir):
    patient_path = os.path.join(base_dicom_dir, patient_dir)

    if not os.path.isdir(patient_path):
        continue

    for date_dir in os.listdir(patient_path):
        date_path = os.path.join(patient_path, date_dir)

        if not os.path.isdir(date_path):
            continue

        for sequence_dir in os.listdir(date_path):
            sequence_path = os.path.join(date_path, sequence_dir)

            if not os.path.isdir(sequence_path):
                continue

            result = convert_dicom_to_nifti(sequence_path)

            # Check if the conversion was successful
            if result.returncode == 0:
                print(f"Converted DICOM to compressed NIfTI in sequence: {sequence_path}")
                # Delete the DICOM files if the conversion was successful
                for file in os.listdir(sequence_path):
                    if file.endswith('.dcm'):
                        os.remove(os.path.join(sequence_path, file))
            else:
                print(f"Error converting DICOM to compressed NIfTI in sequence: {sequence_path}")
                print(result.stderr)

print("Finished converting DICOM files to compressed NIfTI format.")
