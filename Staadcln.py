
import pandas as pd
import re
import numpy as np

# Function to separate the first integer to Column A and rest to Column B
def separate_data(row):
    elements = str(row).split()
    if len(elements) == 0:
        return pd.Series([None, None])
    
    first_element = elements[0]
    if '.' in first_element:
        first_element = first_element.split('.')[0]
    
    rest_elements = " ".join(elements[1:])
    
    return pd.Series([first_element, rest_elements])

# Function to replace specific characters with a semicolon beside the digits of the fourth float or integer
# and remove any instances of \][{}/~ regardless of their location
def clean_and_replace(row):
    # Replace "—" with "-"
    row = row.replace("—", "-")
    
    # Replace specified characters beside the fourth float or integer with a semicolon
    step1_cleaned = re.sub(r'(\S+ \S+ \S+ \S+)[~\[\]{}\/()]', r'\1;', str(row))
    
    # Remove any remaining instances of \][{}/~ regardless of their location
    final_cleaned = re.sub(r'[~\[\]{}\/()]', '', step1_cleaned)
    
    return final_cleaned

# Load the Excel file into a DataFrame
original_df = pd.read_excel('Book1.xlsx')  # Update this path

# Apply the function to separate the data into two columns
separated_data = original_df.iloc[:, 0].apply(separate_data)
separated_data.columns = ['Column A', 'Column B']

# Remove rows with NaN values or empty strings
separated_data.replace('', np.nan, inplace=True)  # Replace empty strings with NaN
separated_data.dropna(inplace=True)  # Remove rows with NaN values

# Apply the cleaning and replacing function to Column B
separated_data['Final Cleaned Column B'] = separated_data['Column B'].apply(clean_and_replace)

# Save the DataFrame with the final cleaned Column B to a new Excel file
separated_data.to_excel('Cleaned_Separated_Book1.xlsx', index=False)  # Update this path
