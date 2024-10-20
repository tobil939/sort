import os
import pandas as pd
import shutil
import logging

# Log file 
logging.basicConfig(
    filename='sort.txt',
    level=logging.DEBUG,
    format ='%(asctime)s - %(levelname)s - %(message)s'
)
#logging.debug('Nachrtcht')
#logging.info('Nachricht')
#logging.warning('Nachricht')
#logging.error('Nachricht')
#logging.critical('Nachricht')

#F = "Osci1"
#F = "Osci2"
#A = "Motor"
#A = "Gen"
#ending = ".trc"
#ending = ".png"

# Data file
current_path = os.getcwd()
file_path = 'prz1.xlsx'
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
    return df.apply(lambda x: str(abs(x)) if isinstance(x, (int, float)) else '99')

# Create folders
def create_folder():
    for folder in folders100 + folders75 + folders50 + folders25:
        os.makedirs(folder, exist_ok=True)
        logging.info('Ordner wurden erstellt')

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
    logging.info('Daten wurden eingelesen')

    return datam100, datam75, datam50, datam25, datag100, datag75, datag50, datag25

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
    logging.info('Daten wurden umgewandelt')
    
    return datam100_array, datam75_array, datam50_array, datam25_array, datag100_array, datag75_array, datag50_array, datag25_array

# Print Data
def print_data(arrays):
    for array in arrays:
        print(array)
        logging.info('Arry %s wurde ausgegeben', array)

# Sort Data for mat files
def sort_data_mat(tosort):
    logging.info('Sortierung von %s wurde gestartet .mat', tosort)
    B = tosort.iloc[0, 1]  # Value from the first row, second column

    strings = []
    
    target_path = None

    #select the path 
    if (tosort is datam100):
        target_path = "RT100/Motor/Fups"
    elif (tosort is datam75):
        target_path = "RT75/Motor/Fups"
    elif (tosort is datam50):
        target_path = "RT50/Motor/Fups"
    elif (tosort is datam25):
        target_path = "RT25/Motor/Fups"
    elif (tosort is datag100):
        target_path = "RT100/Gen/Fups"
    elif (tosort is datag75):
        target_path = "RT75/Gen/Fups"
    elif (tosort is datag50):
        target_path = "RT50/Gen/Fups"
    elif (tosort is datag25):
        target_path = "RT25/Gen/Fups"

    if target_path is None:
        logging.error('kein gültiger Pfad')
        return
    
    for j in range(2, 10):
        C = int(tosort.iloc[1, j])
    

        # Loop through the rows (from index 2 to 14)
        for i in range(2, 15):
            logging.info('for Loop für D gestartet %s', i)
            D = tosort.iloc[i, 0]  # Value from the current row, first column
            #j = tosort.iloc[1].tolist().index(C)  # Index of the column for C
            DD = str(D) + "rpm"

            # Determine E
            try:
                E = int(tosort.iloc[i, j])
                logging.info('es wird nach E gesucht')
            except IndexError:
                E = 99  # Fallback value if no matching cell is found
                logging.warning('Es wurde eine leere Zelle gefunden')


            EE = str(E) + "Nm"
            # Create string
            result_string = f"A: {A}, B: {B}, C: {C}, D: {D}, E: {E}, F: {F}"
            strings.append(result_string)
            logging.info('string wurde erstellt')

            # Search for .trc files
            logging.info('es wird nach .trc gesucht in %s', current_path)
            for filename in os.listdir(os.getcwd()):
                logging.debug('Datei gefunden %s', filename)
                if filename.endswith('.mat'):
                    logging.debug('überprüfen ob D E und E im Namen sind %s', filename)
                    # Check if D, E, and C are in the filename
                    if str(DD) in filename and str(EE) in filename and str(C) in filename and str(A) in filename:
                        source_file = os.path.join(os.getcwd(), filename)
                        target_file = os.path.join(target_path, filename)
                        logging.info('Datei gefunden %s', filename)

                        # Move the file
                        shutil.move(source_file, target_file)
                        logging.info('Datei verschoben nach %s', target_path)
                    else:
                        logging.debug('Datei hat nicht D und E im Namen %s', filename)


        
# Sort Data
def sort_data(tosort):
    logging.info('Sortierung von %s wurde gestartet', tosort)
    #A = tosort.iloc[0, 0]  # Motor (first row, first column)
    B = tosort.iloc[0, 1]  # Value from the first row, second column
    #C = int(tosort.iloc[1, 1])  # Value from the second row, second column
    strings = []

    target_path = None

    #select the path
    if (tosort is datam100 and F == "Osci1" and A == "Motor"):
        target_path = "RT100/Motor/Osci1"
    elif (tosort is datam100 and F == "Osci2" and A == "Motor"):
        target_path = "RT100/Motor/Osci2"
    elif (tosort is datam75 and F == "Osci1" and A == "Motor"):
        target_path = "RT75/Motor/Osci1"
    elif (tosort is datam75 and F == "Osci2" and A == "Motor"):
        target_path = "RT75/Motor/Osci2"
    elif (tosort is datam50 and F == "Osci1" and A == "Motor"):
        target_path = "RT50/Motor/Osci1"
    elif (tosort is datam50 and F == "Osci2" and A == "Motor"):
        target_path = "RT50/Motor/Osci2"
    elif (tosort is datam25 and F == "Osci1" and A == "Motor"):
        target_path = "RT25/Motor/Osci1"
    elif (tosort is datam25 and F == "Osci2" and A == "Motor"):
        target_path = "RT25/Motor/Osci2"
    elif (tosort is datag100 and F == "Osci1" and A == "Gen"):
        target_path = "RT100/Gen/Osci1"
    elif (tosort is datag100 and F == "Osci2" and A == "Gen"):
        target_path = "RT100/Gen/Osci2"
    elif (tosort is datag75 and F == "Osci1" and A == "Gen"):
        target_path = "RT75/Gen/Osci1"
    elif (tosort is datag75 and F == "Osci2" and A == "Gen"):
        target_path = "RT75/Gen/Osci2"
    elif (tosort is datag50 and F == "Osci1" and A == "Gen"):
        target_path = "RT50/Gen/Osci1"
    elif (tosort is datag50 and F == "Osci2" and A == "Gen"):
        target_path = "RT50/Gen/Osci2"
    elif (tosort is datag25 and F == "Osci1" and A == "Gen"):
        target_path = "RT25/Gen/Osci1"
    elif (tosort is datag25 and F == "Osci2" and A == "Gen"):
        target_path = "RT25/Gen/Osci2"

    if target_path is None:
        logging.error('kein gültiger Pfad')
        return

    #os.makedirs(target_path, exist_ok=True)
    
    for j in range(2, 10):
        C = int(tosort.iloc[1, j])
    

        # Loop through the rows (from index 2 to 14)
        for i in range(2, 15):
            logging.info('for Loop für D gestartet %s', i)
            D = tosort.iloc[i, 0]  # Value from the current row, first column
            #j = tosort.iloc[1].tolist().index(C)  # Index of the column for C
            DD = str(D) + "rpm"

            # Determine E
            try:
                E = int(tosort.iloc[i, j])
                logging.info('es wird nach E gesucht')
            except IndexError:
                E = 99  # Fallback value if no matching cell is found
                logging.warning('Es wurde eine leere Zelle gefunden')


            EE = str(E) + "Nm"
            # Create string
            result_string = f"A: {A}, B: {B}, C: {C}, D: {D}, E: {E}, F: {F}"
            strings.append(result_string)
            logging.info('string wurde erstellt')

            # Search for .trc files
            logging.info('es wird nach .trc gesucht in %s', current_path)
            for filename in os.listdir(os.getcwd()):
                logging.debug('Datei gefunden %s', filename)
                if filename.endswith(ending):
                    logging.debug('überprüfen ob D E und E im Namen sind %s', filename)
                    # Check if D, E, and C are in the filename
                    if str(DD) in filename and str(EE) in filename and str(C) in filename and str(F) in filename and str(A) in filename:
                        source_file = os.path.join(os.getcwd(), filename)
                        target_file = os.path.join(target_path, filename)
                        logging.info('Datei gefunden %s', filename)

                        # Move the file
                        shutil.move(source_file, target_file)
                        logging.info('Datei verschoben nach %s', target_path)
                    else:
                        logging.debug('Datei hat nicht D und E im Namen %s', filename)

    # Output the generated strings
    #for s in strings:
    #    print(s)
    #    logging.info('strings werden ausgegeben')

# Main Loop
create_folder()
for e in range(1,3):
    if e == 1:
        ending = ".trc"
    elif e == 2:
        ending = ".png"
    for f in range(1,3):
        if f == 1:
            F = "Osci1"
        elif f == 2:
            F = "Osci2"
        read_data()
        #arrays = convert_data()
        arrays = read_data()
        #print_data(arrays)
        for a in range(1,3):
            if a == 1:
                A = "Gen"
            elif a == 2:
                A = "Motor"
            for array in arrays:
                sort_data(array)

for a in range(1,3):
    if a == 1:
        A = "Gen"
    elif a == 2:
        A = "Motor"
    for array in arrays:
        sort_data_mat(array)

