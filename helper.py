from os import listdir, remove
from os.path import join, isfile

# Returns true if extension is valid
def valid_extension(filename):
    extensions = {"png", "jpg", "jpeg"}
    return filename[-3:] in extensions
    
# Removes the first file from local_image directory
def clear_dir():
    
    path = join("local_image", listdir("local_image")[0])

    if isfile(path):
        remove(path)

    
