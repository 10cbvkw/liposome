import mrcfile
import numpy as np
import re
import os
from scipy.io import savemat

def read_mrc_file(filepath):
    """Reads an image from an MRC file."""
    with mrcfile.open(filepath, mode='r') as mrc:
        return mrc.data

def parse_circle_info(filepath):
    """Parses center coordinates and radius from a text file."""
    center_x, center_y, radius = [], [], []
    with open(filepath, 'r') as f:
        for line in f:
            match = re.search(r'Center\s*=\s*\((\d+),\s*(\d+)\),\s*Radius\s*=\s*([\d.]+)', line)
            if match:
                center_x.append(int(match.group(1)))
                center_y.append(int(match.group(2)))
                radius.append(float(match.group(3)))
    return np.array(center_x).reshape(-1, 1).astype(np.float64), np.array(center_y).astype(np.float64).reshape(-1, 1), np.array(radius).reshape(-1, 1)

def convert_to_mat(image_file, circle_info_file, output_file):
    """Converts an MRC image and circle information to a MAT file."""
    # Read MRC image
    mMicrograph = read_mrc_file(image_file)

    # Parse circle info
    dVesicleCntX, dVesicleCntY, dVesicleR = parse_circle_info(circle_info_file)

    # Save to MAT file
    mat_data = {
        'dVesicleCntX': dVesicleCntX,
        'dVesicleCntY': dVesicleCntY,
        'dVesicleR': dVesicleR, 
        'mMicrograph': mMicrograph
    }
    savemat(output_file, mat_data)

def process_all_files(mrc_folder, txt_folder, output_folder):
    """Processes all .mrc and .txt files in the given folders."""
    mrc_files = [f for f in os.listdir(mrc_folder) if f.endswith('.mrc')]
    txt_files = [f for f in os.listdir(txt_folder) if f.endswith('.txt')]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    iter_ = 0
    for mrc_file in mrc_files:
        base_name = os.path.splitext(mrc_file)[0]
        txt_file = f'{base_name}_centers_and_radii.txt'

        if txt_file in txt_files:
            mrc_path = os.path.join(mrc_folder, mrc_file)
            txt_path = os.path.join(txt_folder, txt_file)
            output_path = os.path.join(output_folder, f'MicData_{iter_}.mat')
            iter_ += 1

            convert_to_mat(mrc_path, txt_path, output_path)
            print(f'Processed: {mrc_file} and {txt_file} into {output_path}')
        else:
            print(f'No matching .txt file for {mrc_file}')

if __name__ == "__main__":
    # Adjust these folder paths as needed
    mrc_folder = 'mrc'
    txt_folder = 'output'
    output_folder = 'mat'

    process_all_files(mrc_folder, txt_folder, output_folder)