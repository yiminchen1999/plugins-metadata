
import pandas as pd
import urllib.request
import io
import re
import fitz
import os
import pandas as pd

txt_directory = "1995papers_output"
xlsx_file = "CSCL_1995_revised.xlsx"
df = pd.read_excel('/Users/chenyimin/PycharmProjects/plugins-quickstart/CSCL_1995.xlsx', engine='openpyxl')
df["content"] = ""

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
                content = "".join(line.split("\t")[1] for line in lines[3:])  # Skip the first 3 lines and take the second column
            else:
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

            # Get the first line of the content
            first_line = content.split("\n")[0].strip()

            # Match the first line with the title column
            title_match = df[df["title"] == first_line]

            # If there is a match, update the content column with the matched title
            if not title_match.empty:
                df.at[index, "content"] = title_match["title"].values[0]

df.to_excel(xlsx_file, index=False)


