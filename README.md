![NIH logo](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/NIH_Logo_Broad.png)

## NIH Molecular Imaging Branch - Deep Learning Preprocessing Tools

This repository shares the preprocessing scripts we use at the NIH Molecular Imaging Branch. Depending on your raw data and your labels several preprocessing steps are needed before Deep Learning models can be trained. This repository focuses mainly on Computer Vision and Natural Language Processing tasks.

### Contents

*Computer Vision
    **[1. Image patch extractor for VOI files](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/VOI_PROCESSING.md)** The VOI file format is used to save medical imaging segmentations. Although not very common, it is still used by some applications e.g. Brainmaker or NIH MIPAV. With this [library](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/voi_processing.py) image patches and masks can be created based on segmentations in VOI format.

*Natural Language Processing
    **[2. DOC/DOCX document converter](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/WORD_CONVERTER.md)** Microsoft Office switched from the old DOC format to the XML based DOCX format in 2003. This format is more suitable for Natural Language Processing since extracting strings and parsing text is pretty straightforward. This [script](https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing/blob/master/word_converter.py) converts DOC files to DOCX files or vice versa and can be run directly in the command line.
