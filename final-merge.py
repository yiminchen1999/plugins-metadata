import os
import pandas as pd

def merge_xlsx_files(input_folder, output_file):
    # Get a list of all XLSX files in the input folder
    files = [file for file in os.listdir(input_folder) if file.endswith('.xlsx')]

    # Check if there are any files to merge
    if not files:
        print("No XLSX files found in the input folder.")
        return

    # Initialize an empty DataFrame to store the merged data
    merged_data = pd.DataFrame()

    # Loop through each file and merge its data into the DataFrame
    for file in files:
        file_path = os.path.join(input_folder, file)
        df = pd.read_excel(file_path)
        merged_data = pd.concat([merged_data, df], ignore_index=True)

    # Save the merged DataFrame to a new XLSX file
    merged_data.to_excel(output_file, index=False)
    print(f"Successfully merged {len(files)} files into {output_file}.")

if __name__ == "__main__":
    input_folder = "path/to/your/input/folder"
    output_file = "path/to/your/output/file.xlsx"
    merge_xlsx_files(input_folder, output_file)
