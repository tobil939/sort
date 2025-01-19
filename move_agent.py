# ==================== Agent zum Verschieben von Daten
# Aktuell ist es als Baustein in AD gedacht und keine eigenständiger Agent
# Nach jedem 5 Schritt wird geschaut ob der Inhalt auf dem Y Ordner größer 30GB ist.
# Falls ja, wird das vershieben auf das Mexx Laufwerkt angestoßen.
# Solange verschoben wird, kann kein neues Verschieben angestoßen werden.
# Inhalt des Y Ordners wird zum Zeitpunkt des Überprüfens martkiert.
# Daten die nach dem angestoßen hinzukommen, sollten daher nicht verschoben werden.
# Version 1.0           2025-01-19
# Änderungslog:

# ========== Verwendete Bibliotheken


import os
import shutil


# ========== Moving Agent
def moving_agent(fromADcounter, fromADmoving, fromADfolderY, fromADfolderMexx):
    # ==================== Variablen
    counter = fromADcounter
    move_bit = fromADmoving
    folder1_path = fromADfolderY
    folder2_path = fromADfolderMexx

    # ==================== Freier Speicher ermitteln
    def get_free_space(folder):
        stat = os.statvfs(folder)
        return stat.f_bavail * stat.f_frsize

    # ==================== Belegter Speicher
    def get_folder_size(folder):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for n in filenames:
                i = os.path.join(dirpath, n)
                total_size += os.path.getsize(i)
        return total_size

    # ==================== Fehlercode setzen
    def set_error_code(free_space, folder1_size, move_bit):
        if free_space <= folder1_size:
            return 1  # Kein freier Speicher
        elif move_bit:
            return 2  # Es wird gerade verschoben
        else:
            return 0  # Alles ok

    # ==================== Daten verschieben
    def move_data(folder1_path, folder2_path, move_bit):
        snapshot = os.listdir(folder1_path)
        for item in snapshot:
            fromfolder = os.path.join(folder1_path, item)
            tofolder = os.path.join(folder2_path, item)

            if os.path.isdir(fromfolder):
                if not os.path.exists(tofolder):
                    os.makedirs(tofolder)
                move_bit = move_data(fromfolder, tofolder, move_bit)
            else:
                if not os.path.exists(
                    tofolder
                ):  # Datei nur verschieben, wenn sie noch nicht existiert
                    shutil.move(fromfolder, tofolder)
                    move_bit = True
        return move_bit

    # ==================== Hauptprogramm
    free_space = get_free_space(folder2_path)
    folder1_size = get_folder_size(folder1_path)

    error = set_error_code(free_space, folder1_size, move_bit)

    if error == 0 and counter >= 5:
        move_bit = move_data(folder1_path, folder2_path, move_bit)
        counter = 0  # Zähler zurücksetzen

    return error, move_bit, counter
