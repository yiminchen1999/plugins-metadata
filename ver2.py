import docx
import pandas as pd

def extract_content_from_docx(docx_file, title):
    doc = docx.Document(docx_file)
    content = []
    for paragraph in doc.paragraphs:
        content.append(paragraph.text)
    content = '\n'.join(content)
    start_index = content.find(title)
    if start_index != -1:
        end_index = content.find('\n', start_index)
        return content[start_index:end_index]
    return ''

# Replace with the path to your Excel file
excel_file_path = 'CSCL_1995.xlsx'

# Replace with the name of the Excel sheet where your data is located
sheet_name = 'Sheet1'

# Replace with the column name that contains the paper titles
title_column = 'title'

# Replace with the path to your Word document
docx_file_path = '1995.docx'

# Read the Excel file
df = pd.read_excel('/Users/chenyimin/PycharmProjects/plugins-quickstart/CSCL_1995.xlsx', engine='openpyxl')

# Create a new column named 'Content'
df['Content'] = ''

# Iterate over each row
for index, row in df.iterrows():
    title = row[title_column]
    content = extract_content_from_docx(docx_file_path, title)
    df.at[index, 'Content'] = content
# Save the updated DataFrame to the Excel file
df.to_excel('/Users/chenyimin/PycharmProjects/plugins-quickstart/1995output_ver3.xlsx', index=False)

