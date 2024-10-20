import pandas as pd
import os
import shutil

file_path = 'prz.xlsx'  # Korrigiere den Pfad zu deiner Datei
source_path = os.getcwd()  # Aktuelles Verzeichnis

# Einlesen der Daten mit fillna für leere Zellen
datam100 = pd.read_excel(file_path, usecols='B:K', skiprows=1, nrows=15).fillna(99)
datam75 = pd.read_excel(file_path, usecols='M:V', skiprows=1, nrows=15).fillna(99)
datam50 = pd.read_excel(file_path, usecols='X:AK', skiprows=1, nrows=15).fillna(99)
datam25 = pd.read_excel(file_path, usecols='AI:AR', skiprows=1, nrows=15).fillna(99)
datag100 = pd.read_excel(file_path, usecols='B:K', skiprows=18, nrows=15).fillna(99)
datag75 = pd.read_excel(file_path, usecols='M:V', skiprows=18, nrows=15).fillna(99)
datag50 = pd.read_excel(file_path, usecols='X:AK', skiprows=18, nrows=15).fillna(99)
datag25 = pd.read_excel(file_path, usecols='AI:AR', skiprows=18, nrows=15).fillna(99)

# Funktion zur Umwandlung der Daten in Strings
def process_dataframe(df):
    return df.applymap(lambda x: str(abs(x)) if isinstance(x, (int, float)) else '99')

# Anwendung der Funktion auf die DataFrames
datam100_array = process_dataframe(datam100).to_numpy()
datam75_array = process_dataframe(datam75).to_numpy()
datam50_array = process_dataframe(datam50).to_numpy()
datam25_array = process_dataframe(datam25).to_numpy()
datag100_array = process_dataframe(datag100).to_numpy()
datag75_array = process_dataframe(datag75).to_numpy()
datag50_array = process_dataframe(datag50).to_numpy()
datag25_array = process_dataframe(datag25).to_numpy()

# Ausgabe der bearbeiteten Arrays
print("Data M100 mit 99 gefüllten Werten:")
print(datam100_array)

print("\nData G25 mit 99 gefüllten Werten:")
print(datag25_array)

# Werte aus den spezifischen Zellen extrahieren
A = datam100.iloc[0, 0]  # Motor (Spalte 1, Zeile 0)
B = datam100.iloc[0, 1]  # Wert von Zeile 1, Spalte 2
C = int(datam100.iloc[1, 1])  # Wert von Zeile 2, Spalte 2

strings = []

# Dateien finden
target_path = 'heinz'

# Stelle sicher, dass das Zielverzeichnis existiert, andernfalls erstelle es
os.makedirs(target_path, exist_ok=True)

# Schleife über die Zeilen von D (Zeile 3 bis 15, d.h. von 2 bis 14 im 0-basierten Index)
for i in range(2, 15):
    D = datam100.iloc[i, 0]  # Wert von Zeile i, Spalte 1
    
    # Spaltenindex für C ermitteln
    column_index_C = datam100.iloc[1].tolist().index(C)  # Index der Spalte von C

    # E ermitteln: Wert in der gleichen Spalte wie C und der Zeile von D
    try:
        # Hier verwenden wir den Wert von D als Zeilenindex (0-basiert)
        E = int(datam100.iloc[i, column_index_C])
    except IndexError:
        E = 99  # Fallback-Wert, falls keine passende Zelle gefunden wird
    
    # String erstellen
    result_string = f"A: {A}, B: {B}, C: {C}, D: {D}, E: {E}"
    strings.append(result_string)

    # Durchsuche das Quellverzeichnis nach .trc-Dateien
    print(f"Durchsuche: {source_path} nach .trc-Dateien...")
    for filename in os.listdir(source_path):
        print(f"Gefundene Datei: {filename}")  # Debugging-Ausgabe
        # Überprüfen, ob die Datei eine .trc-Datei ist
        if filename.endswith('.trc'):
            print(f"Überprüfe Datei: {filename}")  # Debugging-Ausgabe
            # Überprüfen, ob einer der Werte (D oder E) im Dateinamen enthalten ist
            if str(D) in filename and str(E) in filename and str(C) in filename:
                # Vollständige Pfade für die Quelle und das Ziel erstellen
                source_file = os.path.join(source_path, filename)
                target_file = os.path.join(target_path, filename)

                # Verschiebe die Datei
                shutil.move(source_file, target_file)
                print(f"Verschoben: {filename} nach {target_path}")
            else:
                print(f"Dateiname {filename} enthält nicht {D} oder {E}.")  # Debugging-Ausgabe

# Ausgabe der generierten Strings
for s in strings:
    print(s)

