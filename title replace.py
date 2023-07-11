import os
import os

folder_path = "1997papers1"  # Replace with the actual folder path

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        range_str, ext = os.path.splitext(filename)
        start_point, _ = range_str.split("-")
        new_filename = start_point + ext
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))


print("Files renamed and saved to the '1997_revised' folder.")