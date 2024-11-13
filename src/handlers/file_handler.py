import os
import time

# Check if the raw data file exists.
def check_file(file_name: str) -> bool:
    if os.path.exists(file_name):
        return True
    return False

# Move the file into the sheets directory with the new name.
def move_file(src: str, dest: str) -> None:
    while not check_file(src):
        time.sleep(1)

    # Clean up the destination file if it exists.
    if check_file(dest):
        os.remove(dest)

    # Move the raw data file into the sheets directory.
    os.rename(src, dest)