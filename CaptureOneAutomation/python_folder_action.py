#!/bin/python3

import os
import time
import subprocess

folder_path = "/Volumes/imeswaprod/Projects/Boeing/Imaging/TestAutomatedC1Processing"
flag_file_name = "script_activated.flag"

def script_activated(folder_path, flag_file_name):
    return os.path.exists(os.path.join(folder_path, flag_file_name))

def set_script_activated_flag(target_folder, flag_file_name):
    with open(os.path.join(target_folder, flag_file_name), "w") as flag_file:
        flag_file.write("This is a flag file to indicate that the script has already been run.")

def run_applescript(script_name):
    subprocess.run(["osascript", script_name])

def find_cosessiondb_files(folder_path):
    cosessiondb_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".cosessiondb"):
                cosessiondb_files.append(os.path.join(root, file))
    return cosessiondb_files

def open_with_capture_one(file_path):
    app_name = "Capture One 23"
    subprocess.run(["open", "-a", app_name, file_path])

if not script_activated(folder_path, flag_file_name):
    if os.path.exists(folder_path) and os.listdir(folder_path):
        cosessiondb_files = find_cosessiondb_files(folder_path)

        if cosessiondb_files:
            file_to_open = cosessiondb_files[0]
            
            # Get the folder containing the .cosessiondb file
            cosessiondb_folder = os.path.dirname(file_to_open)

            if not script_activated(cosessiondb_folder, flag_file_name):

            
                open_with_capture_one(file_to_open)
                print(f"Opened file: {file_to_open}")


                # Set the flag in the folder containing the .cosessiondb file
                set_script_activated_flag(cosessiondb_folder, flag_file_name)

                # Wait for 10 seconds
                time.sleep(10)

                # Run the AppleScript
                applescript_name = "/Volumes/imeswaprod/Projects/Boeing/Archived/KentPythonToolbox/C1Automation/AutoScriptC1.scpt"
                print("pre-flag")
                run_applescript(applescript_name)
                print("Flag")

        else:
            print("No files with the '.cosessiondb' extension were found.")
    else:
        print("The 'AutomatedC1Processing' folder is either non-existent or empty.")
else:
    print("The script has already been run for this folder.")
