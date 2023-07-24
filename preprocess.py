import os
import pandas as pd


def convert_csv_to_xlsx(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            csv_path = os.path.join(folder_path, filename)
            xlsx_path = os.path.join(folder_path, filename.replace(".csv", ".xlsx"))

            # Read the CSV file
            df = pd.read_csv(csv_path)

            # Convert to XLSX and skip writing the index
            df.to_excel(xlsx_path, index=False)

            # Read the XLSX file to modify it
            df = pd.read_excel(xlsx_path)

            # Delete the first row (index 0)
            df = df.iloc[1:]

            # Delete the 'id' column (assuming it's named 'id')
            df = df.drop(columns=['id'], errors='ignore')

            # Save the modified DataFrame back to the XLSX file
            df.to_excel(xlsx_path, index=False)


if __name__ == "__main__":
    folder_path = "ISLS_1995-2021"  # Replace this with the path to your folder containing CSV files
    convert_csv_to_xlsx(folder_path)
