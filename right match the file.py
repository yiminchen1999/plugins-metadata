import pandas as pd

# Read the Excel file
df = pd.read_excel('ISLS_1995-2021/CSCL_2011.xlsx')

# Rename the column to 'id'
df.rename(columns={'dc.identifier.uri[]': 'id'}, inplace=True)
# Convert 'id' column to string type
df['id'] = df['id'].astype(str)

# Create a new DataFrame with the updated 'id' column
new_df = df.copy()
new_df['id'] = new_df['id'].apply(lambda uri: str(uri).split('.')[-1])

# Save the modified DataFrame back to the Excel file
new_df.to_excel('CSCL_2011_revised_11.xlsx', index=False)

print("Files saved with renamed column.")


