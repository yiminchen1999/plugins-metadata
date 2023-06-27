
import pandas as pd
import urllib.request
import io
import re
import fitz
import os
import pandas as pd

txt_directory = "1997papers_output"
xlsx_file = "CSCL_1997_without_title_author.xlsx"
df = pd.read_excel('/Users/chenyimin/PycharmProjects/plugins-quickstart/CSCL_1997.xlsx', engine='openpyxl')
df["content"] = ""

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Get the ID from the first column
    id_value = str(row["id"])
    txt_file_path = os.path.join(txt_directory, id_value + ".txt")

    #
    if os.path.isfile(txt_file_path):
        with open(txt_file_path, "r", encoding="latin-1") as txt_file:
            lines = txt_file.readlines()
            content = " ".join(lines[7:])  # Skip the first 7 lines (title, author, abstract)

        df.at[index, "content"] = content

df.to_excel(xlsx_file, index=False)

