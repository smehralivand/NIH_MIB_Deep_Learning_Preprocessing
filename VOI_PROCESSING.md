## VOI Processing Library

We use this python library to facilitate the preprocessing of label contours saved in voi format. The whole library is based on the VoiPatient class, which represents a patient scan and related
voi files. The class is initialized by the full path to the patient folder passed as a string. The two main methods are save_bb_patches() and save_masks(), which save bounding box patches and image masks of the voi files in 8-bit png format, respectively. You can either import the library to your python project or copy and paste the whole code into your python file.

### Code Examples

```python
from voi_processing import VoiPatient

patient_scan = VoiPatient('C:/Documents/Scans/Patient_001') # Use forward slashes in Windows

patient_scan.save_bb_patches('C:/Documents/Patient_001/Patches')
```

Reads the dicom and voi files in C:\Documents\Scans\Patient_001 and saves bounding box patches of this scan in C:\Documents\Patient_001\Patches.

```python
from voi_processing import VoiPatient

patient_scan = VoiPatient('C:/Documents/Scans/Patient_001') # Use forward slashes in Windows

patient_scan.save_masks('C:/Documents/Patient_001/Masks')
```

Reads the dicom and voi files in C:\Documents\Scans\Patient_001 and saves image masks and corresponding dicom image slices in C:\Documents\Patient_001\Masks.

***Using os library***

```python
import os
from voi_processing import VoiPatient

main_folder = 'C:/Documents/Dataset' # Use forward slashes in Windows

for folder in os.listdir(main_folder):
    folder = os.path.join(main_folder, folder)
    patient_scan = VoiPatient(folder)
    patient_scan.save_masks('C:/Documents/Masks')
```

Iterates over all patients scans in folder C:\Documents\Dataset and saves all masks and corresponding dicom image slices in C:\Documents\Masks.

***Using pathlib library***

```python
from pathlib import Path
from voi_processing import VoiPatient

main_folder = Path('C:/Users/mehralivands/Desktop/Bone Lesion Dataset - Processed') # Use forward slashes in Windows

for folder in main_folder.iterdir():
    patient_scan = VoiPatient(folder)
    patient_scan.save_masks('C:/Users/mehralivands/Desktop/temp')
```

Iterates over all patients scans in folder C:\Documents\Dataset and saves all masks and corresponding dicom image slices in C:\Documents\Masks.
