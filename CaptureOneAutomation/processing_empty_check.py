#!/bin/python3

import os
import sys
import shutil
import json
import logging
import urllib
import time
from pathlib import Path


#path for hold folder for C1 automation
processing_path = '/Volumes/imeswaprod/Projects/Boeing/Imaging/TestAutomatedC1Processing'
#path for folder where C1 processes images
hold_path = '/Volumes/imeswaprod/Projects/Boeing/Imaging/TestReadyForExport'
#path for empty shell folders
empty_complete_path = '/Volumes/imeswaprod/Projects/Boeing/Imaging/TestExportComplete'
#path for QC
qchold_path = '/Volumes/imeswaprod/Projects/Boeing/Imaging/04_ReadyForQC-HOLD'
#path for QC
qc_path = '/Volumes/imeswaprod/Projects/Boeing/Imaging/04_ReadyForQC'
#path source
sourcehold_path = '/Volumes/imeswaprod/Projects/Boeing/Imaging/01_Source-HOLD'
#path source
source_path = '/Volumes/imeswaprod/Projects/Boeing/Imaging/01_Source'


def main():
    global source_path
    global qc_path
    global processing_path
    global hold_path
    global empty_complete_path

    
    dir = os.listdir(processing_path)
    print("begin")
    #if processing is not happening
    if len(dir) == 1:
        print("Processing empty")

        #EDITS
    
        src_dir = '/Volumes/imeswaprod/Projects/Boeing/Imaging/TestReadyForExport'
        dst_dir = '/Volumes/imeswaprod/Projects/Boeing/Imaging/TestExportComplete'
    
        # Get a list of all subdirectories in the source directory
        subdirs = [os.path.join(src_dir, d) for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]

        # Iterate over the subdirectories
        for subdir in subdirs:
            # Check if the subdirectory is empty
            if not os.listdir(subdir):
                # If it is, move it to the destination directory
                shutil.move(subdir, dst_dir)
                print(f"Moved empty directory {subdir} to {dst_dir}")
            
                # Create a flag file within the moved folder
                flag_file = os.path.join(dst_dir, os.path.basename(subdir), os.path.basename(subdir) + '.flag')
                os.makedirs(os.path.dirname(flag_file), exist_ok=True)
                with open(flag_file, 'w') as f:
                    f.write('This folder has been moved.')
                print(f"Created flag file {flag_file}")
        #EDITS
        
        #count for whether a file was moved to processing
        moved = 0
        #boolean to maintain search until a file is found
        search = True
        #walks folders to find cosession files and move parent directories
        for root, dirs, files in os.walk(hold_path):
            #files in hold folder
            for file in files:
                if file.endswith(".cosessiondb"):
                    if moved == 0:
                        print("moving")
                        #moves folder to process if it has not been done already
                        shutil.move(os.path.abspath(root), processing_path)
                        #iterates move to not allow other folders to be moved
                        moved = moved+1
                        search = False
        #checks to see if there are empty folders to move
        for folder in os.listdir(hold_path):
            if len(os.path.join(hold_path,folder)) == 1:
                print("moving empty parent")
                #moves empty parent folder to be joined later
                shutil.move(os.path.join(hold_path, folder), empty_complete_path)
    #list of keywords that define a folder as a subfolder
    subList = ["_120", "_4x5", "_35"]
    #checks complete path to tie up loose parent directories with children
    for folder in os.listdir(empty_complete_path):
        print("checking for merges in complete")
        #name of sub folder to merge
        folderName = str(folder)
        print(folderName)
        if "_120" in folderName or "_35" in folderName or "_4x5" in folderName:
            head, tail = folderName.split('_',1)
            #new collection of folders to find the empty one to put the subfolder into
            for secondFolder in os.listdir(empty_complete_path):
                    secondFolderName = str(secondFolder)
                    if "_120" in secondFolderName:
                        print("nothing")
                    elif "_35" in secondFolderName:
                        print("nothing")
                    elif "_4x5" in secondFolderName:
                        print("nothing")
                    elif head in secondFolderName:
                        shutil.move(os.path.join(empty_complete_path, folder), os.path.join(empty_complete_path, secondFolder))
                    
                    
                    
                    
                
            
            

if __name__=="__main__":
    main()


