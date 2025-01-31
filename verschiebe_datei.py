import os
import shutil


def verschiebe_datei(sSortFile, sSourceFolder, sTargetFolderJoint):
    """
    Verschiebt eine Datei von einem Quellordner in einen Zielordner.
    Falls der Zielordner nicht existiert, wird er erstellt.

    :param sSortFile: Name der zu verschiebenden Datei
    :param sSourceFolder: Quellordner der Datei
    :param sTargetFolderJoint: Zielordner der Datei
    """
    try:
        # Pfad zur Quelldatei
        source_path = os.path.join(sSourceFolder, sSortFile)

        # Pfad zum Zielordner und Datei
        target_path = os.path.join(sTargetFolderJoint, sSortFile)

        # Überprüfen, ob der Zielordner existiert, ansonsten erstellen
        if not os.path.exists(sTargetFolderJoint):
            os.makedirs(sTargetFolderJoint)

        # Datei verschieben
        shutil.move(source_path, target_path)
        print(
            f"Die Datei {sSortFile} wurde erfolgreich von {sSourceFolder} nach {sTargetFolderJoint} verschoben."
        )

    except FileNotFoundError:
        print(f"Fehler: Die Datei {sSortFile} wurde im Quellordner nicht gefunden.")
    except PermissionError:
        print(f"Fehler: Keine Berechtigung, um die Datei {sSortFile} zu verschieben.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
