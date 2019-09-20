![NIH logo](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/NIH_Logo_Broad.png)

## NIH Molecular Imaging Branch - Deep Learning Preprocessing Tools

This repository shares the preprocessing scripts we use at the Molecular Imaging Branch at the NIH. Depending on your raw data and your labels and annotations several preprocessing steps are needed before the Deep Learning models can be actually trained. This repository focuses mainly on computer vision tasks. Natural Language Processing tools are in planned.

### Contents

**1. NIfTI file anonymization.** When collaborating with external institutions or industry patient data needs to be anonymized reliably. Since the DICOM header data is not consistent and extendable using NIfTI files instead is usually considered a safer alternative. With this tool NIfTI files can be safely anonymized.

**2. VOI to NIfTI mask conversion.** VOI is a rarely used file format created by the NIH software MIPAV (Medical Image Processing, Analysis and Visualization, https://mipav.cit.nih.gov/) mainly used for saving segmentations made on DICOM images. here you will find tools to convert VOI files to NIfTI masks. Since NIfTI files can be anonymized more easily and safely we also offer tools for converting DICOM images or whole scans to NIfTY files.
