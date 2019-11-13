#!/usr/bin/env python3
#-------------------------------------------------------------------------------
# Author: Samira Masoudi
# Date:   11.07.2019
#-------------------------------------------------------------------------------
from __future__ import print_function
import argparse
import sys
import SimpleITK as sitk
from os import mkdir,listdir,makedirs
import numpy as np
import csv
import cv2
import re
import pandas as pd
from os.path import isdir,join,exists

def normalize(arr, N=255, eps=1e-6):
    """
    To normalize an image by mapping its [Min,Max] into the interval [0,255]
    :param arr: Input (2D or 3D) array of image
    :param N: Scaling factor
    :param eps:
    :return: Normalized Image
    """
    arr = arr.astype(np.float32)
    output = N*(arr-np.min(arr))/(np.max(arr)-np.min(arr)+eps)
    return output

def Physical2array(array, origin, spacing):
    """
    To convert an input physical values based on the Origin and Spacing of the original image
    :param array: Physical values
    :param origin: Origin of axes in the original image
    :param spacing: Spacing of the axes in the original image
    :return: Converted physical values into array
    """
    origin = origin(...,np.newaxis)
    spacing = spacing(..., np.newaxis)
    array -= origin
    output = array//spacing
    return output.astype(int)

def get_ROI_slice_loc(voi_path,org,spc):
        """
        To extract the labels in form of coordinates
        :param voi_path: Path to the .voi file where labels are stored. Note that labels descibe the of a certain lesion is specified at different slides,
        you can find the sample version of the labels in data folder.
        :param org: Origin of the physical array
        :param spc: spacing of the physical array
        :return: A dictionary of the extracted labels:{slide number 1:[[x0,y0],[x1,y1],[x2,y2],...],...}
        """
        voi_df = pd.read_fwf(voi_path)
        first_line = []
        last_line = []
        slice_number=[]
        loc_dict = {}

        # collecting the slice numbers with the first and last line describing the label coordinates in .voi file
        for line in range(len(voi_df)): # Go through the .voi file line by line
            line_specific = voi_df.iloc[line, :] # Read each line
            # We used the specific characteristics in the content of the .voi file which may be specific to our annotation tool (Radiant)
            # Sample organization of the first 13 lines in our .voi file:
                    # MIPAV VOI FILE
                    # 255  # color of VOI - red component
                    # 0  # color of VOI - green component
                    # 0  # color of VOI - blue component
                    # 255  # color of VOI - alpha component
                    # 1  # number of slices for the VOI
                    # 5  # slice number
                    # 1  # number of contours in slice
                    # 64  # number of pts in contour <Chain-element-type>1</Chain-element-type>
                    # 261.409  309.846
                    # 261.01 309.775
                    # 260.583 309.564

            # Please change these code according to the contents of your annotation file
            as_list = line_specific.str.split(r"\t\t")[0] # Get the describing title at each line
            if "# slice number" in as_list: # In case we are at the line which specifies the slice number,
                slice_number.append(int(as_list[0])) # take the slice number
                first_line.append(line+3) # First line of coordinates starts right after 3 lines under the slice number
            if "# number of pts in contour <Chain-element-type>1</Chain-element-type>" in as_list:# Where the coordinates end
                last_line.append(line+int(as_list[0]))


        # Now we start reading the coordinates from first to the last line for each slice.
        for i in range(len(first_line)):
            # For each labeled slice:
            counter=0
            X = np.zeros((last_line[i] + 1 - first_line[i] , 1))
            Y = np.zeros((last_line[i] + 1 - first_line[i] , 1))
            for j in range(first_line[i],last_line[i]+1):
                    # reading coordinates line by line
                    line_specific = voi_df.iloc[j,:]
                    Coords_str = line_specific.str.split(r"\t")[0][0]
                    for m in re.finditer("\d+.\d+\s", Coords_str):
                        Y[counter] = float(m.group(0))
                    for m in re.finditer("\s\d+.\d+", Coords_str):
                        X[counter] = float(m.group(0))
                    counter += 1
            # Here we have the labels aligned with arrays, otherwise we had to convert the physical values specified
            # by labels into their equivalent index of the arrays
            # coords = Physical2array(np.hstack((X,Y)), org, spc)
            loc_dict.update({slice_number[i]: np.hstack((X,Y)).astype(int)})
            del X, Y
        return loc_dict

def Dicom_series_Reader (Input_path):
    """
    Reading Dicom files from Input path
    :param Input_path: path to dicom folder which contains dicom slices
    :return: 3D Array of the dicom image as well as Origin and Spacing of the image regarding the physical array
    """
    print("Reading Dicom directory:", Input_path )
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(Input_path)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    size = image.GetSize()
    # print("Image size:", size[0], size[1], size[2])
    # # Convert the image to a  numpy array first and then shuffle the dimensions to get axis in the order z,y,x
    ct_scan = sitk.GetArrayFromImage(image)
    # print('CT scan has the shape of:', ct_scan.shape)
    # # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(image.GetOrigin())))
    # print('Origin of the CT scan:', origin)
    # # Read the spacing along each dimension
    spacing = np.array(list(reversed(image.GetSpacing())))
    # print('spacing of the CT scan:', spacing)
    return ct_scan,origin,spacing

def clip(Slice,WL,WW):
    """
    Clipping or windowing the Input 2D slice
    :param Slice: Input 2D array
    :param WL: Wl is the center of the threshold interval
    :param WW: WW is half the length of the threshold interval
    :return: Input 2D array which values are clipped at [WL-WW, WL+WW]
    """
    Slice[Slice < (WL - WW)] = np.floor(WL - WW)
    Slice[Slice > (WL + WW)] = np.floor(WL + WW)
    return Slice


def dicom2patch():

        # ---------------------------------------------------------------------------
        # Parse the commandline
        # ---------------------------------------------------------------------------
        parser = argparse.ArgumentParser(description='Extracting Labeled patches from dicom images at dicom_folder and save the results at target_folder')
        parser.add_argument('--dicom_folder', type=str, default='C:\\Users\\masoudis2\\Desktop\\Bone_data_test', help='Input path')
        parser.add_argument('--target_folder', type=str, default='C:\\Users\\masoudis2\\Desktop\\Bone_CT_classification', help='Output path')
        parser.add_argument('--image_type', type=str, default=['png','npy'], help='Image type requested at the output, options are \'png\', \'jpeg\' and \'npy\'')
        parser.add_argument('--WL', type=int, default=300, help='Window Center')
        parser.add_argument('--WW', type=int, default=1000, help='Window Width')
        args = parser.parse_args()

        print('[i] Input directory:         ', args.dicom_folder)
        print('[i] Output directory:       ', args.target_folder)
        print('[i] Patch images are saved in forms of:        ', args.image_type)
        print('[i] Center of windowing threshold:             ', args.WL)
        print('[i] Length of windowing interval:           ', 2*args.WW)

        # Creating folders to save the results
        if 'png' in args.image_type:
            if not exists(join(args.target_folder,'train','png_files')):
                makedirs(join(args.target_folder,'train','png_files'))
        if 'jpeg' in args.image_type:
            if not exists(join(args.target_folder, 'train', 'jpeg_files')):
                    makedirs(join(args.target_folder, 'train', 'jpeg_files'))
        if 'npy' in args.image_type:
            if not exists(join(args.target_folder, 'train', 'Numpy')):
                    makedirs(join(args.target_folder, 'train', 'Numpy'))
        #Double check on the requested image type
        Types=['png','jpeg','npy']
        if isinstance(args.image_type,str):
            args.image_type=args.image_type.split(",")
        for i in range(len(args.image_type)):
            if not (args.image_type[i] in Types):
                raise ValueError('Type',args.image_type[i],'is not supported, please consider modifying the code!')

        Folder_Group=listdir(args.dicom_folder)
        for i, folder in enumerate(Folder_Group):
                folder_path = join(args.dicom_folder, folder)
                onlyfolders = [f for f in listdir(folder_path) if isdir(join(folder_path, f))] # We have only one folder that leads to dicom path
                Image_folder = [f for f in listdir(join(folder_path, onlyfolders[0])) if (f[-3:]!="voi" and f!='VERSION')] # Getting the only dicom folder and not the .voi files
                Non_Image_folder = [f for f in listdir(join(folder_path, onlyfolders[0])) if (f!=Image_folder[0] and f!='VERSION')] # getting the labels as .voi files
                Input_path = join(folder_path, onlyfolders[0], Image_folder[0])
                # Reading the image at the Input path
                CT_scan, origin, spacing = Dicom_series_Reader(Input_path)
                # Reading the label files
                for j in range(len(Non_Image_folder)):
                    L_ind = 0
                    # Labeling file Cancerous to 1 vs Benign to 0
                    if re.findall('cancer',Non_Image_folder[j]) or re.findall('Cancer',Non_Image_folder[j]):
                        L_ind=1
                    # Reading the label coordinates
                    loc_dict = get_ROI_slice_loc(join(folder_path,onlyfolders[0],Non_Image_folder[j]), origin, spacing)
                    for key,val in loc_dict.items():
                            Min = np.min(loc_dict[key], axis=0)
                            Max = np.max(loc_dict[key], axis=0)
                            x0 = (Min[0]) if (Min[0]>-1) else 0
                            x1 = (Max[0]) if ((Max[0])<CT_scan[key].shape[0]) else (CT_scan[key].shape[0]-1)
                            y0 = (Min[1]) if (Min[1]>-1) else 0
                            y1 = (Max[1]) if ((Max[1])<CT_scan[key].shape[1]) else (CT_scan[key].shape[1]-1)
                            Slice=normalize(clip(CT_scan[key],WL=args.WL,WW=args.WW))
                            Det_box = Slice[x0:x1, y0:y1]
                            if 'png' in args.image_type:
                                    cv2.imwrite(join(args.target_folder,'train','png_files',folder+ '_'+ Non_Image_folder[j][:-4] + '_' +str(key)+'_'+str(L_ind)+'.png'), Det_box)
                            if 'jpeg' in args.image_type:
                                    cv2.imwrite(join(args.target_folder,'train','jpeg_files',folder+ '_'+ Non_Image_folder[j][:-4] + '_' +str(key)+'_'+str(L_ind)+'.jpg'), Det_box)
                            if 'npy' in args.image_type:
                                     np.save(join(args.target_folder, 'train', 'Numpy', folder + '_' + Non_Image_folder[j][:-4] + '_' + str(key) +'_'+ str(L_ind) + '.npy'), Det_box)
        return 0
if __name__ == '__main__':
    sys.exit(dicom2patch())
