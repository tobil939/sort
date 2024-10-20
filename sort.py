import os
import pandas as pd
import shutil

# Log file 
log_file = "sort.txt"

# Data file
file_path = 'prz.xlsx'
target_path = 'heinz'

# Folder structure
folders100 = [
    "RT100/Motor/Fups/_old",
    "RT100/Motor/Osci1/_old",
    "RT100/Motor/Osci2/_old",
    "RT100/Gen/Fups/_old",
    "RT100/Gen/Osci1/_old",
    "RT100/Gen/Osci2/_old",
]

folders75 = [
    "RT75/Motor/Fups/_old",
    "RT75/Motor/Osci1/_old",
    "RT75/Motor/Osci2/_old",
    "RT75/Gen/Fups/_old",
    "RT75/Gen/Osci1/_old",
    "RT75/Gen/Osci2/_old",
]

folders50 = [
    "RT50/Motor/Fups/_old",
    "RT50/Motor/Osci1/_old",
    "RT50/Motor/Osci2/_old",
    "RT50/Gen/Fups/_old",
    "RT50/Gen/Osci1/_old",
    "RT50/Gen/Osci2/_old",
]

folders25 = [
    "RT25/Motor/Fups/_old",
    "RT25/Motor/Osci1/_old",
    "RT25/Motor/Osci2/_old",
    "RT25/Gen/Fups/_old",
    "RT25/Gen/Osci1/_old",
    "RT25/Gen/Osci2/_old",
]

# Global data variables
datam100 = datam75 = datam50 = datam25 = None
datag100 = datag75 = datag50 = datag25 = None

# Function to convert to string and abs
def process_dataframe(df):
    return df.applymap(lambda x: str(abs(x)) if isinstance(x, (int, float)) else '99')

# Create folders
def create_folder():
    for folder in folders100 + folders75 + folders50 + folders25:
        os.makedirs(folder, exist_ok=True)

# Read Data
def read_data():
    global datam100, datam75, datam50, datam25
    global datag100, datag75, datag50, datag25

    datam100 = pd.read_excel(file_path, usecols='B:K', skiprows=1, nrows=15).fillna(99)
    datam75 = pd.read_excel(file_path, usecols='M:V', skiprows=1, nrows=15).fillna(99)
    datam50 = pd.read_excel(file_path, usecols='X:AK', skiprows=1, nrows=15).fillna(99)
    datam25 = pd.read_excel(file_path, usecols='AI:AR', skiprows=1, nrows=15).fillna(99)
    datag100 = pd.read_excel(file_path, usecols='B:K', skiprows=18, nrows=15).fillna(99)
    datag75 = pd.read_excel(file_path, usecols='M:V', skiprows=18, nrows=15).fillna(99)
    datag50 = pd.read_excel(file_path, usecols='X:AK', skiprows=18, nrows=15).fillna(99)
    datag25 = pd.read_excel(file_path, usecols='AI:AR', skiprows=18, nrows=15).fillna(99)

# Convert Data
def convert_data():
    global datam100, datam75, datam50, datam25
    global datag100, datag75, datag50, datag25

    datam100_array = process_dataframe(datam100).to_numpy()
    datam75_array = process_dataframe(datam75).to_numpy()
    datam50_array = process_dataframe(datam50).to_numpy()
    datam25_array = process_dataframe(datam25).to_numpy()
    datag100_array = process_dataframe(datag100).to_numpy()
    datag75_array = process_dataframe(datag75).to_numpy()
    datag50_array = process_dataframe(datag50).to_numpy()
    datag25_array = process_dataframe(datag25).to_numpy()
    
    return datam100_array, datam75_array, datam50_array, datam25_array, datag100_array, datag75_array, datag50_array, datag25_array

# Print Data
def print_data(arrays):
    for array in arrays:
        print(array)

# Sort Data
def sort_data(tosort):
    A = tosort.iloc[0, 0]  # Motor (first row, first column)
    B = tosort.iloc[0, 1]  # Value from the first row, second column
    C = int(tosort.iloc[1, 1])  # Value from the second row, second column

    strings = []
    os.makedirs(target_path, exist_ok=True)

    # Loop through the rows (from index 2 to 14)
    for i in range(2, 15):
        D = tosort.iloc[i, 0]  # Value from the current row, first column
        column_index_C = tosort.iloc[1].tolist().index(C)  # Index of the column for C

        # Determine E
        try:
            E = int(tosort.iloc[i, column_index_C])
        except IndexError:
            E = 99  # Fallback value if no matching cell is found

        # Create string
        result_string = f"A: {A}, B: {B}, C: {C}, D: {D}, E: {E}"
        strings.append(result_string)

        # Search for .trc files
        print(f"Searching in: {os.getcwd()} for .trc files...")
        for filename in os.listdir(os.getcwd()):
            print(f"Found file: {filename}")  # Debugging output
            if filename.endswith('.trc'):
                print(f"Checking file: {filename}")  # Debugging output
                # Check if D, E, and C are in the filename
                if str(D) in filename and str(E) in filename and str(C) in filename:
                    source_file = os.path.join(os.getcwd(), filename)
                    target_file = os.path.join(target_path, filename)

                    # Move the file
                    shutil.move(source_file, target_file)
                    print(f"Moved: {filename} to {target_path}")
                else:
                    print(f"Filename {filename} does not contain {D} or {E}.")  # Debugging output

    # Output the generated strings
    for s in strings:
        print(s)

# Main Loop
create_folder()
read_data()
arrays = convert_data()
print_data(arrays)

# Assuming you want to sort based on datam100
sort_data(datam100)

