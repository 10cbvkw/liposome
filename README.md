# liposome

## Setup

1. Make a new folder named 'mrc', and put your mrc files here or change the paths in the code.
2. Make a new folder named 'images', and use save_jpg.py to convert mrcfiles to jpgfiles here or change the paths in the code.

## Get centers and radii

1. Install SAM correctly and download vit_h (sam_vit_h_4b8939.pth). Reference: https://github.com/facebookresearch/segment-anything
2. Use operate_sam.py to estimate centers and radii.

## Prepare data

1. Use tomat.py to convert mrcfiles and the coresponding centers and radii to .mat files, which can be used in the vesicle-removing algorithm later.
