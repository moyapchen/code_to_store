# STOLEN FROM https://github.com/roboes/tools/blob/main/sports/tcx-tools.py
# Did change it though to modify from the AllTrails tcx format.  


"""Script that performs a series of transformations to the Training Center XML (.tcx) workout data file."""


###############
# Initial Setup
###############

# Erase all declared global variables
globals().clear()


# Import packages
import glob
import os
import re


# Set working directory
# os.chdir(path=os.path.join(os.path.expanduser('~'), 'Downloads', 'alltrails'))


###########
# Functions
###########


def tcx_lstrip(*, directory):
    """Remove leading first line blank spaces of .tcx activity files."""
    # List of .tcx files including path
    files = glob.glob(pathname=os.path.join(directory, '*.tcx'), recursive=False)

    if len(files) > 0:
        for file in files:
            with open(file=file, encoding='utf-8') as file_in:
                file_text = file_in.readlines()
                file_text_0 = file_text[0]
                file_text[0] = file_text[0].lstrip()

            if file_text[0] != file_text_0:
                with open(file=file, mode='w', encoding='utf-8') as file_out:
                    file_out.writelines(file_text)


def strip_alltrails(file_lines): 
    res = []
    append = True
    for line in file_lines: 
        if "<Folders>" in line: 
            append = False 
            res.append("<Activities>") 

        if "</Course>" in line: 
            append = False
            res.append("</Lap>") 
            res.append("</Activity>")
            res.append("</Activities>") 
            res.append("</TrainingCenterDatabase>") 

        if "<Lap>" in line: 
            append = False

        if append:
            if "<Name>" in line: 
                line = line.replace("Name", "Id")  
            res.append(line)

        if "<Course>" in line: 
            append = True
            res.append('<Activity Sport="running">')

        if "</Lap>" in line: 
            append = True
            res.append("<Lap>") 

    return res

def tcx_process_all(*, directory, filepath_output):
    # List of .tcx files including path
    files = glob.glob(pathname=os.path.join(directory, '*.tcx'), recursive=False)

    # process_all files
    for file in files:
        if not os.path.isfile(file): 
            continue
        print(file)
        with open(file=file, encoding='utf-8') as file_in:
            name = os.path.splitext(os.path.basename(file))[0] 

            file_text = file_in.readlines()
            file_text =   strip_alltrails(file_text)  
            
            text_out = ''.join(file_text)


        with open(file=os.path.join(filepath_output, name + ".tcx"), mode='w', encoding='utf-8') as file_out:
            file_out.writelines(text_out)


############
# .tcx Tools
############

tcx_lstrip(
    directory=os.path.join(
        os.path.expanduser('~'),
        'Downloads',
        'alltrails',
    ),
)

tcx_process_all(
    directory=os.path.join(
        os.path.expanduser('~'),
        'Downloads',
        'alltrails',
    ),
    filepath_output=os.path.join(
        os.path.expanduser('~'),
        'Downloads',
        'alltrails/out',
    ),
)
