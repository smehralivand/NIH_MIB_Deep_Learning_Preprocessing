![NIH logo](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/NIH_Logo_Broad.png)

## NIH Molecular Imaging Branch - Deep Learning Preprocessing Tools

This repository shares the preprocessing scripts we use at the Molecular Imaging Branch at the NIH. Depending on your raw data and your labels several preprocessing steps are needed before the Deep Learning models can be actually trained. This repository focuses mainly on computer vision tasks. Natural Language Processing tools are in planned.

### Contents

**1. [Image patch extractor for VOI files](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/VOI_Extractor.md)** The VOI file format is used to save medical imaging segmentations. Although not very common, it is still used by some applications e.g. Brainmaker or NIH MIPAV. With this [script](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/Lesion_Patch_Extraction.py) image patches can be extracted from DICOM files based on segmentations saved as VOI files.
