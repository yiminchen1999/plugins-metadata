import os

# Define the source folder containing the files
source_folder = '1997papers/'

# Create a new folder for renamed files
new_folder = '1997papers_output/'
os.makedirs(new_folder, exist_ok=True)

# Get the list of files in the source folder
file_list = os.listdir(source_folder)

# Filter the file list to only include txt files
txt_files = [filename for filename in file_list if filename.endswith('.txt')]

# Sort the txt file list based on page numbers
sorted_files = sorted(txt_files, key=lambda x: int(x.split('-')[0]))

# Rename and move the txt files
for index, filename in enumerate(sorted_files):
    # Create the new filename
    new_filename = '1997{}.txt'.format(index + 1)

    # Build the full paths for the source and destination files
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(new_folder, new_filename)

    # Rename and move the file
    os.rename(source_path, destination_path)

print('Files renamed and moved successfully!')


