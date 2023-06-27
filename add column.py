import pandas as pd

import pandas as pd

# Read the Excel file
xlsx_file = 'CSCL_1995.xlsx'
df = pd.read_excel(xlsx_file)

# Create a new column with IDs
df.insert(0, 'id', ['1995{}'.format(index + 1) for index in range(len(df))])

# Save the modified DataFrame back to the Excel file
df.to_excel(xlsx_file, index=False)

print('IDs added to the Excel file successfully!')

