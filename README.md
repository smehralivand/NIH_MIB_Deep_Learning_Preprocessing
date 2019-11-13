![NIH logo](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/NIH_Logo_Broad.png)

## NIH Molecular Imaging Branch - Deep Learning Preprocessing Tools

This repository shares the preprocessing scripts we use at the Molecular Imaging Branch at the NIH. Depending on your raw data and your labels several preprocessing steps are needed before the Deep Learning models can be actually trained. This repository focuses mainly on computer vision tasks and Natural Language Processing.

### Contents

**[1. Image patch extractor for VOI files](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/VOI_Extractor.md)** The VOI file format is used to save medical imaging segmentations. Although not very common, it is still used by some applications e.g. Brainmaker or NIH MIPAV. With this [script](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/Lesion_Patch_Extraction.py) image patches can be extracted from DICOM files based on segmentations saved as VOI files.

**2. [DOC/DOCX document converter](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/MS%20Word%20Document%20Converter.md)** Microsoft Office switched from the old DOC format to the XML based DOCX format in 2003. This format is more suitable for Natural Language Processing since extracting strings and parsing text is pretty straightforward. This [script](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/MS%20Word%20Converter.py) converts DOC files to DOCX files or vice versa and can be run directly in the command line.
