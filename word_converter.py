'''
----------------------------------------------------------------------------------------------------------------------------------------
Author: Sherif Mehralivand
Email: sherif.mehralivand@mail.de
Github: https://github.com/smehralivand/NIH_MIB_Deep_Learning_Preprocessing
Twitter: @smehralivand
Date: 6/9/2020
----------------------------------------------------------------------------------------------------------------------------------------
'''

import os, glob
from tqdm import tqdm
import win32com.client

print('\nNIH Word Converter 1.0\n'.upper())
target_folder = input('Please enter target directory path: ')
os.chdir(target_folder)

while True:

    print('\n1. Convert DOC files into DOCX format.')
    print('\n2. Convert DOCX files into DOC format.')
    print('\n3. End program.')

    inp = input('\nHow do you want to continue? [1-3] ')

    if inp == '1':
        # DOC to DOX conversion
        num = 0
        word = win32com.client.Dispatch("Word.Application")
        word.visible = False
        print('\nConverting files...\n')
        # Saving files with new extension and new format
        for current_file in tqdm(glob.glob('**/*.doc', recursive=True)):
            num += 1
            wb = word.Documents.Open(os.path.abspath(current_file))
            converted_file = os.path.abspath(current_file + 'x')
            wb.SaveAs2(converted_file, FileFormat=16) # file format for DOCX
            wb.Close()
        word.Quit()
        # Removing previous files
        print('\nRemoving previous files...\n')
        for current_file in tqdm(glob.glob('**/*.doc', recursive=True)):
            os.remove(current_file)
        print ('{} files were converted'.format(num))
        break

    elif inp == '2':
        # DOCX to DOC conversion
        num = 0
        word = win32com.client.Dispatch("Word.Application")
        word.visible = False
        print('\nConverting files...\n')
        # Saving files with new extension and new format
        for current_file in tqdm(glob.glob('**/*.docx', recursive=True)):
            num += 1
            wb = word.Documents.Open(os.path.abspath(current_file))
            converted_file = os.path.abspath(current_file)[0:-1]
            wb.SaveAs2(converted_file, FileFormat=0)  # file format for DOC
            wb.Close()
        word.Quit()
        # Removing previous files
        print('\nRemoving previous files...\n')
        for current_file in tqdm(glob.glob('**/*.docx', recursive=True)):
            os.remove(current_file)
        print ('{} files were converted'.format(num))
        break
    
    elif inp == '3':
        break
    
    else:
        print('\nFalse entry. Please try again.\n')
        continue
