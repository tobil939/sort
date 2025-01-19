# ==================== Agent zum Verschieben von Daten
# Aktuell ist es als Baustein in AD gedacht und keine eigenständiger Agent
# Nach jedem Schritt wird geschaut ob der Inhalt auf dem Y Ordner größer 30GB ist.
# Falls ja, wird das vershieben auf das Mexx Laufwerkt angestoßen.
# Solange verschoben wird, kann kein neues Verschieben angestoßen werden.
# Inhalt des Y Ordners wird zum Zeitpunkt des Überprüfens martkiert.
# Daten die nach dem angestoßen hinzukommen, sollten daher nicht verschoben werden.
# Version 3.0           2025-01-19
# Änderungslog:
# Zu viel um es hier rein zu schreiben!

# ========== Verwendete Bibliotheken
import os
import shutil

# ========== Variablen von AD
move_bit = False
error = False
fromADmaxsize = 30 * 1024**3
fromADfolderY = "Y:/bunga/baunga/hart"
fromADfolderMexx = "M:/bunga/bunga/hart"


# ========== Moving Agent
def moving_agent(fromADmaxsize, fromADfolderY, fromADfolderMexx, error):
    # ==================== Variablen
    folder1_path = fromADfolderY
    folder2_path = fromADfolderMexx
    max_size = fromADmaxsize

    # ==================== Freier Speicher ermitteln
    def get_free_space(folder):
        try:
            stat = os.statvfs(folder)  # Dateistatistik abrufen
            return stat.f_bavail * stat.f_frsize  # freier Speicher in Byte
        except Exception as e:
            print(f"Error when determing the free memory: {e}")
            error = True
        return 0, error

    # ==================== Belegter Speicher
    def get_folder_size(folder):
        total_size = 0
        try:
            # Alle Dateien im Unterordern durchlaufen
            for dirpath, dirnames, filenames in os.walk(folder):
                for n in filenames:  # Verstehe ich selbst nicht
                    i = os.path.join(dirpath, n)  # Bestimmt wichtig
                    total_size += os.path.getsize(
                        i
                    )  # Summiert die einzelenen Größen zusammen
            return total_size
        except Exception as e:
            print(f"Error when determing memory size: {e}")
            error = True
        return 0, error

    # ==================== Fehlercode setzen
    def set_status_code(free_space, folder1_size, move_bit):
        try:
            if free_space <= folder1_size:
                return 1  # Kein freier Speicher
            elif move_bit:
                return 2  # Es wird gerade verschoben
            elif folder1_size < max_size:
                return 3  # 30GB sind noch nicht erreicht
            else:
                return 0  # Alles ok
        except Exception as e:
            print(f"Error when determing status: {e}")
            error = True
        return 4, error

    # ==================== Daten verschieben
    def move_data(folder1_path, folder2_path, move_bit):
        try:
            move_bit = True
            snapshot = os.listdir(folder1_path)  # Istaufnahme des Ordnerinhaltes
            for item in snapshot:  # item ist der Dateiname
                fromfolder = os.path.join(
                    folder1_path, item
                )  # Vollständiger Pfad mit Dateiname bauen
                tofolder = os.path.join(folder2_path, item)  # wie oben

                # Wenn es sich um einen Ornder handeklt
                if os.path.isdir(fromfolder):  # ist es eine Ordner?
                    if not os.path.exists(
                        tofolder
                    ):  # Wenn der Ordner noch nicht existiert am Ziel
                        os.makedirs(tofolder)  # Ornder erstellen
                        # move_data(fromfolder, tofolder, move_bit) # Endlosschleife?
                    else:
                        shutil.move(fromfolder, tofolder)  # verschieben
                else:
                    # Wenn es sich um eine Datei handelt
                    if not os.path.exists(
                        tofolder
                    ):  # Datei nur verschieben, wenn sie noch nicht existiert
                        shutil.move(fromfolder, tofolder)  # verschieben
                        move_bit = False
            return move_bit
        except Exception as e:
            print(f"Error during moving: {e}")
            nonlocal error
            error = True
        return move_bit, error

    # ==================== Hauptprogramm
    try:
        if os.path.exists(folder1_path) and os.path.isdir(folder1_path):
            print("bunga")
    except Exception as e:
        print(f"Path not found: {e}")
        error = True
        return error

    try:
        if os.path.exists(folder2_path) and os.path.isdir(folder2_path):
            print("bunga")
    except Exception as e:
        print(f"Path not found: {e}")
        error = True
        return error

    free_space = get_free_space(folder2_path)
    folder1_size = get_folder_size(folder1_path)

    status = set_status_code(free_space, folder1_size, move_bit)

    if not error:
        if folder1_size > max_size and status == 0:
            move_bit = move_data(folder1_path, folder2_path, move_bit)
        return status, move_bit
    else:
        print("There is a Problem")
    return status, move_bit, error


status = moving_agent(fromADmaxsize, fromADfolderY, fromADfolderMexx, error)

print(f"Error: {error}")


if status == 1:
    print("Not enough storage space on the target drive")
elif status == 2:
    print("Data is currently being moved")
elif status == 3:
    print("The size of 30GB has not yet been reached")
elif status == 4:
    print("There was an Exception")
