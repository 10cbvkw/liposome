import scipy.io
import mrcfile
import numpy as np

def save_micrograph_to_mrc(mat_file_path, mrc_file_path):
    # Load data from the .mat file
    mat_data = scipy.io.loadmat(mat_file_path)

    # Extract the micrograph data
    mMicrograph = mat_data['mMicrographVesiclesSubtracted']

    # Ensure the data is in float32 format for MRC file compatibility
    if mMicrograph.dtype != np.float32:
        mMicrograph = mMicrograph.astype(np.float32)

    # Create a new MRC file
    with mrcfile.new(mrc_file_path, overwrite=True) as mrc:
        mrc.set_data(mMicrograph)
        print(f"Micrograph has been saved to {mrc_file_path}")

# Example usage
mat_file_path = '/Users/yez/Desktop/pose_analyze/JSB2-maxR-60-iShapeInterpMet-2-iShiftFreq-6-iShiftAmpl-7-PC-24-R8-A3-after-vesicle-subtraction-mic-11.mat' 
mrc_file_path = 'output_micrograph.mrc'    

save_micrograph_to_mrc(mat_file_path, mrc_file_path)