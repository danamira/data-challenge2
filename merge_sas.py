import os
import pandas as pd

# Directory containing the subdirectories
main_dir = 'data/crime'

# Initialize an empty list to store DataFrames
dfs = []

# Iterate over each subdirectory in the main directory
for subdir in os.listdir(main_dir):
    subdir_path = os.path.join(main_dir, subdir)
    print(subdir)
    # Check if the path is a directory
    if os.path.isdir(subdir_path):
        # Get the month from the directory name
        month = subdir

        # Iterate over each file in the subdirectory
        file = '{}-metropolitan-stop-and-search.csv'.format(month)

        print(file)

        file_path = os.path.join(subdir_path, file)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Add the month column
        df['month'] = month

        # Append the DataFrame to the list
        dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
final_df = pd.concat(dfs, ignore_index=True)

# Export the data as a single `.csv` file for future use
final_df.to_csv('data/processed/sas_merged.csv')
