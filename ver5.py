
import pandas as pd
import urllib.request
import io
import re
import fitz
import os
import pandas as pd

# Path to the directory containing the TXT files
txt_directory = "1995papers_output"

# Path to the XLSX file
xlsx_file = "CSCL_1995.xlsx"

# Read the Excel file
df = pd.read_excel('/Users/chenyimin/PycharmProjects/plugins-quickstart/CSCL_1995.xlsx', engine='openpyxl')

# Create an empty "content" column
df["content"] = ""

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Get the ID from the first column
    id_value = str(row["id"])

    # Create the path to the corresponding TXT file
    txt_file_path = os.path.join(txt_directory, id_value + ".txt")

    # Check if the TXT file exists
    if os.path.isfile(txt_file_path):
        # Read the content from the TXT file
        with open(txt_file_path, "r", encoding="latin-1") as txt_file:
            content = txt_file.read()

        # Assign the content to the "content" column in the DataFrame
        df.at[index, "content"] = content

# Save the modified DataFrame back to the XLSX file
df.to_excel(xlsx_file, index=False)

