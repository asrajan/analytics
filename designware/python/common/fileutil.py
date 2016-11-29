"""
module : fileutil

Defines a file utilities that can be commonly used
"""

from os import path
import re

def is_tiff(file):
    """ Returns true if the file name is a tiff file 
    Args:
        file : a string representing the file name
    Note : This function looks at the file extension to determine
    whether the file is tiff or not
    """
    root,ext = path.splitext(file)
    if ext.lower() == ".tiff" or ext.lower() == ".tif":
        return True
    else:
        return False

def is_hidden_file(file):
    """ Returns true if the file is a hidden system file """
    h_files = [r"Thumbs\.db$", r".*.ini$", r"\.DS_STORE"]
    for h_file in h_files:
        h_file_re = re.compile(h_file)
        if h_file_re.search(file):
            return True
    return False




