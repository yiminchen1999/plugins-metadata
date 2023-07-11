import pandas as pd
import os

folder_path = "1995 Papers"  # Replace with the actual folder path

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        range_str, ext = os.path.splitext(filename)
        start_point, _ = range_str.split("-")
        new_filename = start_point + ext
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

print("Files renamed and saved to the '1995_revised' folder.")
# Read the Excel file
df = pd.read_excel('CSCL_1995_fullcopy.xlsx')


# Rename the column to 'id'
df.rename(columns={'dc.identifier.uri[]': 'id'}, inplace=True)
# Convert 'id' column to string type
df['id'] = df['id'].astype(str)

# Create a new DataFrame with the updated 'id' column
new_df = df.copy()
new_df['id'] = new_df['id'].apply(lambda uri: str(uri).split('.')[-1])

# Save the modified DataFrame back to the Excel file
new_df.to_excel('CSCL_1995_revised_11.xlsx', index=False)

print("Files saved with renamed column.")


import urllib.request
import io
import re
import fitz
import os
import pandas as pd
#记得改地址
txt_directory = "1995 Papers"
xlsx_file = "CSCL_1995_revised.xlsx"
df = pd.read_excel('CSCL_1995_revised_11.xlsx', engine='openpyxl')
df["text"] = ""

#
for index, row in df.iterrows():
    # Get the ID from the first column
    id_value = str(row["id"])

    # Create the path to the corresponding TXT file
    txt_file_path = os.path.join(txt_directory, id_value + ".txt")


    if os.path.isfile(txt_file_path):

        with open(txt_file_path, "r", encoding="latin-1") as txt_file:
            lines = txt_file.readlines()

            # Identify the format
            num_columns = len(lines[0].split("\t"))
            if num_columns == 1:
                # single-column
                content = "".join(lines[3:])  # Skip the first 3 lines (title, author, abstract)
            elif num_columns == 2:
                # Two-column
                content = "".join(
                    line.split("\t")[1] for line in lines[3:])  # Skip the first 3 lines and take the second column
            else:
                # =
                content = ""

            # Find the line index where the introduction part starts
            introduction_start_index = 0
            abstract_found = False
            for i, line in enumerate(lines):
                if "abstract" in line.lower():
                    abstract_found = True
                if "introduction" in line.lower() and not abstract_found:
                    introduction_start_index = i
                    break

            # Join the lines
            content = "".join(lines[introduction_start_index:])

            # Normalize spacing
            content = re.sub(r"\s+", " ", content).strip()

        # Assign the content to the "text" column in the DataFrame
        df.at[index, "text"] = content
df["id"] = "1995" + df["id"].astype(str)
df.rename(columns={'dc.contributor.author[]': 'author'}, inplace=True)
df.rename(columns={'dc.identifier.uri': 'uri'}, inplace=True)
df.to_excel(xlsx_file, index=False)