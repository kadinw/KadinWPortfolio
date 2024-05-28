#!/bin/python3

import os
import shutil

# Function to check if a folder is empty
def is_empty_folder(folder_path):
    content = [item for item in os.listdir(folder_path) if item != ".DS_Store"]
    return len(content) == 0

# Main function to move empty subfolders
def move_empty_subfolders(source_folder, destination_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through subfolders in the source folder
    for folder_name in os.listdir(source_folder):
        if folder_name == ".DS_Store":
            continue

        folder_path = os.path.join(source_folder, folder_name)

        # Check if it's a directory and if it's empty
        if os.path.isdir(folder_path) and is_empty_folder(folder_path):
            # Move the empty subfolder to the destination folder
            shutil.move(folder_path, os.path.join(destination_folder, folder_name))
            print(f'Moved empty folder: {folder_name}')

# Specify the source folder and destination folder
source_folder = '/Volumes/imeswaprod/Projects/Boeing/Imaging/TestReadyForExport'
destination_folder = '/Volumes/imeswaprod/Projects/Boeing/Imaging/TestExportComplete'

# Call the main function
move_empty_subfolders(source_folder, destination_folder)
