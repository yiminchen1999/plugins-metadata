import pandas as pd

# Replace 'input_file.xlsx' and 'output_file.xlsx' with the appropriate file names
input_file_path = 'merged_paper.xlsx'
output_file_path = 'merged_paper_ver2.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(input_file_path)

# Filter rows with blank values in the 'text' column
df = df.dropna(subset=['text'])

# Save the updated DataFrame back to a new Excel file
df.to_excel(output_file_path, index=False)

print("Rows with blank values in 'text' column removed and saved to", output_file_path)
