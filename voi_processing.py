'''
----------------------------------------------------------------------------------------------------------------------------------------
Author: Sherif Mehralivand
Email: sherif.mehralivand@mail.de
Github: https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing
Twitter: @smehralivand
Date: 7/2/2020

Dependencies:
Python 3.6
Pathlib 1.0.1
Numpy 1.18.5
Scipy 1.5.0
Pillow 6.2.1
Scikit-Image 0.16.2
Open-CV 3.4.2
Pydicom 2.0.0
----------------------------------------------------------------------------------------------------------------------------------------
'''

import os
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.ndimage as ndimage
from PIL import Image, ImageDraw
from skimage import draw
import cv2
import pydicom

class VoiPatient:
    '''
    This class represents a patient scan and related voi files. Instances are initialed by the full path to the patient folder
    containing the dicom and voi files passed as a string. All methods are performed on this folder. To process a folder containing
    several patients scans you can implement instances of this class in a for loop. Please check our Github page for code examples.
    '''
    def __init__(self, patient_folder):
        self.patient_folder = Path(patient_folder)

    def min_max_scale(array, lower = 0, upper = 1):
        '''
        This function performs min-max normalization on a numpy array. By standard, scales the array between 0 and 1.
        Input - array: A numpy array to be scaled, lower: Lower boundary, upper: Upper boundary.
        Output - A numpy array scaled between lower and upper boundary.
        '''
        return (((array - array.min()) / (array.max() - array.min())) * (upper - lower)) + lower

    def sorted_dicom(dicom_path):
        '''
        This function sorts dicom files in a folder based on their z axis (SliceLocation tag).
        Input - dicom_path: A file path containing dicom files
        Output - a list of sorted dcm file paths
        '''
        lstFilesDCM = [file_path for file_path in dicom_path.rglob('*.dcm')]
        lstFilesDCM_z = [(dcm_file, float(pydicom.read_file(str(dcm_file)).SliceLocation)) for dcm_file in lstFilesDCM]
        lstFilesDCM_sort = [file_path[0] for file_path in sorted(lstFilesDCM_z, key = lambda tup: tup[1])]
        return lstFilesDCM_sort

    def extract_dicom(dicom_path):
        '''
        This function extracts all dicom images from a path and returns a numpy array of shape
        (slice, width, height). By standard, the images are scaled and saved as 8-bit integers (on the scan level).
        Input - The full path of the VOI file
        Output - A numpy array of shape (slice, width, height) containing all images in the dicom folder in 8-bit integer format.
        '''
        lstFilesDCM = VoiPatient.sorted_dicom(dicom_path)
        pixel_list = []
        for path in lstFilesDCM:
            ds = pydicom.read_file(str(path))
            pixel_list.append(ds.pixel_array)
        return VoiPatient.min_max_scale(np.array(pixel_list), 0, 255).astype(np.uint8)

    def extract_coordinates(voi_path):
        '''
        This function extracts the x, y coordinates from a VOI file.
        Input - The full path of the VOI file
        Output - A Python dictionary of numpy arrays with the slice number as the index and the [x, y] coordinates as arrays
        '''
        voi_df = pd.read_fwf(voi_path)
        voi_dict = {}
        slice_nr = 0
        temp_list = []
        for row in voi_df.iloc[:, 0]:
            if 'slice number' in row:
                slice_nr = int(row.split()[0])
            if '.' in row:
                x = float(row.split(' ')[0])
                y = float(row.split(' ')[1])
                temp_list.append([x,y])
            if slice_nr != 0:
                temp_arr = np.array(temp_list, dtype='float32')
                voi_dict[slice_nr] = temp_arr
        return voi_dict

    def extract_bb_patch(image, contour):
        '''
        This function inputs a numpy image array of shape (pixel width, pixel height) and a numpy VOI segmentation array
        of shape (number of segmentation points, 2) and outputs a numpy image array of the bounding box based on the VOI contour.
        Input - image: A numpy array of the corresponding image, contour: A numpy array of the corresponding VOI contour.
        Output - A numpy array of the bounding box patch.
        '''
        x_min = int(contour[:, 0].min())
        x_max = int(contour[:, 0].max())
        y_min = int(contour[:, 1].min())
        y_max = int(contour[:, 1].max())
        return image[y_min:y_max, x_min:x_max]

    def create_cont_mask(img_size, contour, value = 1):
        '''
        This function inputs a numpy image array of shape (pixel width, pixel height) and a numpy VOI segmentation array
        of shape (number of segmentation points, 2) and outputs a binary (0, 1) numpy mask array of the segmentation
        based on the VOI contour.
        Input - img_size: A tuple of the corresponding image's (width, height), contour: A numpy array of the
        corresponding VOI contour, value: An integer representing the value (category) of the mask. 
        Output - A numpy array of the contour mask.
        '''
        contour_list = []
        for i in range(contour.shape[0]):
            contour_list.append((contour[i, 0], contour[i, 1]))
        contour = contour_list

        img = Image.new('L', img_size, 0)
        try:
            ImageDraw.Draw(img).polygon(contour, outline=value, fill=value)
        except:
            print('Error: Mask could not be created.')
        else:
            img_mask = np.array(img)
            img_mask = ndimage.binary_fill_holes(img_mask)
            img_mask = img_mask.astype(np.uint8)
            img_mask[img_mask==1] = value
            return img_mask

    def save_bb_patch(dicom_folder, voi_path, target_folder):
        '''
        This function inputs a folder containing dicom images and a single VOI file and saves bounding box patches
        in the target folder.
        Input - dicom_folder: A pathlib folder containing the dicom images, voi_path: A pathlib path of a VOI file,
        target_folder: A pathlib folder of the target folder where the extracted patches are to be saved.
        Output - None, saves patches in target folder.
        '''
        target_folder.mkdir(exist_ok=True, parents=False)
        img = VoiPatient.extract_dicom(dicom_folder)
        pts = VoiPatient.extract_coordinates(voi_path)
        for key, contour in pts.items():
            file_name = '_'.join((dicom_folder.parts[-1], voi_path.stem, str(key)))
            file_name = ''.join((file_name, '.png'))
            file_path = Path(target_folder / file_name)
            patch = VoiPatient.extract_bb_patch(img[key], contour)
            print(f'{file_name}')
            cv2.imwrite(file_path.as_posix(), patch)

    def save_mask(dicom_folder, voi_path, target_folder):
        '''
        This function inputs a folder containing dicom images and a single VOI file and saves contour masks
        in the target folder.
        Input - dicom_folder: A pathlib folder containing the dicom images, voi_path: A pathlib path of a VOI file,
        target_folder: A pathlib folder of the target folder where the extracted contour masks are to be saved.
        Output - None, saves patches in target folder.
        '''
        target_folder.mkdir(exist_ok=True, parents=False)
        img = VoiPatient.extract_dicom(dicom_folder)
        pts = VoiPatient.extract_coordinates(voi_path)
        mask_dim = (img.shape[1], img.shape[2])
        for key, contour in pts.items():
            img_file_name = '_'.join((dicom_folder.parts[-1], voi_path.stem, str(key)))
            img_file_name = ''.join((img_file_name, '.png'))
            mask_file_name = '_'.join((dicom_folder.parts[-1], voi_path.stem, str(key)))
            mask_file_name = '_'.join((mask_file_name, 'mask'))
            mask_file_name = ''.join((mask_file_name, '.png'))
            img_file_path = Path(target_folder / img_file_name)
            mask_file_path = Path(target_folder / mask_file_name)
            mask = VoiPatient.create_cont_mask(mask_dim, contour, 255)  
            print(f'{mask_file_name}')
            cv2.imwrite(mask_file_path.as_posix(), mask) # save mask
            print(f'{img_file_name}')
            cv2.imwrite(img_file_path.as_posix(), img[key]) # save corresponding image  

    def save_bb_patches(self, target_folder):
        '''
        This method inputs a folder containing dicom images and a folder with corresponding VOI files and saves
        bounding box patches in the target folder.
        Input - dicom_folder: A pathlib folder containing the dicom images, voi_folder: A pathlib folder containing
        the VOI files, target_folder: A pathlib folder of the target folder where the extracted patches are to be saved.
        Output - None, saves patches in target folder.
        '''
        target_folder = Path(target_folder)
        print(f'\nSaving patches in {target_folder.as_posix()}\n')
        for voi_file in self.patient_folder.rglob('*.voi'):
            VoiPatient.save_bb_patch(self.patient_folder, voi_file, target_folder)

    def save_masks(self, target_folder):
        '''
        This method inputs a folder containing dicom images and a single VOI file and saves contour masks
        in the target folder.
        Input - dicom_folder: A pathlib folder containing the dicom images, voi_path: A pathlib path of a VOI file,
        target_folder: A pathlib folder of the target folder where the extracted masks are to be saved.
        Output - None, saves masks in target folder.
        '''
        target_folder = Path(target_folder)
        print(f'\nSaving masks and corresponding image slices in {target_folder.as_posix()}\n')
        for voi_file in self.patient_folder.rglob('*.voi'):
            VoiPatient.save_mask(self.patient_folder, voi_file, target_folder)