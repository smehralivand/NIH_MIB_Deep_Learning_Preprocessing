## VOI Image Patch Extractor

This script extracts image patches from DICOM files based on segmentations stored in VOI format and saves them either as NumPy files
or image files. The file and folder structure needs to be as follows in order to work correctly:

- X:\main\ - main folder
- X:\main\case\folder1 - Folder with VOI files
- X:\main\case\folder1\folder2 - Folder with DICOM files

### Documentation

Use the help function to get more information about arguments:

python Lesion_Patch_Extraction.py --help

### Code Examples

python Lesion_Patch_Extraction.py --dicom_folder=C:\\Main --target_folder=C:\\Target --image_type=png

Extracts patches from C:\Main and stores them in C:\Target in PNG format using (default) bone windowing with WL = 300 and WW = 1000

python Lesion_Patch_Extraction.py --dicom_folder=C:\\Main --target_folder=C:\\Target --image_type=npy --WL=600 WW=1500

Extracts patches from C:\Main and stores them in C:\Target in NPY format using lung windowing with WL = 600 and WW = 1500
