import os
import shutil
import pydicom


# Function to determine if a sequence is 3D based on the DICOM files within
def is_sequence_3d(sequence_path):
    # Track unique image positions to determine if there are multiple slices
    image_positions = set()

    # Iterate through all files in the sequence directory
    for filename in os.listdir(sequence_path):
        if not filename.endswith('.dcm'):
            continue

        try:
            dicom_path = os.path.join(sequence_path, filename)
            dicom_data = pydicom.dcmread(dicom_path, stop_before_pixels=True)
            image_position = dicom_data.get('ImagePositionPatient', None)

            # If 'ImagePositionPatient' is not present, we assume it's 2D
            if image_position is None:
                return False

            # Use the z-coordinate of 'ImagePositionPatient' to identify unique slices
            image_positions.add(image_position[2])
        except Exception as e:
            print(f"Error reading DICOM file {filename}: {e}")
            # If there's an error, we conservatively assume it's 2D
            return False

    # If there's more than one unique position, we assume the sequence is 3D
    return len(image_positions) > 1


# Base directory where all the patient directories are stored
base_dicom_dir = 'DCM-NII-SLICED'  # Update this path to the location of your DICOM files

# Iterate over each patient directory
for patient_dir in os.listdir(base_dicom_dir):
    patient_path = os.path.join(base_dicom_dir, patient_dir)

    # Skip if not a directory
    if not os.path.isdir(patient_path):
        continue

    # Iterate over each date directory for the patient
    for date_dir in os.listdir(patient_path):
        date_path = os.path.join(patient_path, date_dir)

        # Skip if not a directory
        if not os.path.isdir(date_path):
            continue

        # Iterate over each sequence directory within the date directory
        for sequence_dir in os.listdir(date_path):
            sequence_path = os.path.join(date_path, sequence_dir)

            # Skip if not a directory
            if not os.path.isdir(sequence_path):
                continue

            # Check if the sequence is 3D; if not, delete it
            if not is_sequence_3d(sequence_path):
                shutil.rmtree(sequence_path)
                print(f"Deleted non-3D sequence: {sequence_path}")

print("Finished processing and cleaning up 2D sequences.")
