## VOI Processing Library

We use this python library to facilitate the preprocessing of label contours saved in voi format. The whole library is based on the VoiPatient class, which represents a patient scan and related
voi files. The class is initialized by the full path to the patient folder passed as a string. The two main methods are save_bb_patches() and save_masks(), which save bounding box patches and image masks of the voi files in 8-bit png format, respectively. You can either import the library to your python project or copy and paste the whole code into your python file.

### Code Examples

```python
from voi_processing import VoiPatient

patient_scan = VoiPatient('C:\Documents\Scans\Patient_001')

patient_scan.save_bb_patches('C:\Documents\Patient_001\Patches')
```

Reads the dicom and voi files in folder C:\Documents\Scans\Patient_001 and saves bounding box patches of this scan in folder C:\Documents\Patient_001\Patches.

```python
from voi_processing import VoiPatient

patient_scan = VoiPatient('C:\Documents\Scans\Patient_001')

patient_scan.save_masks('C:\Documents\Patient_001\Masks')
```

Reads the dicom and voi files in folder C:\Documents\Scans\Patient_001 and saves image masks and corresponding dicom image slices in folder C:\Documents\Patient_001\Masks.

