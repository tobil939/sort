import os
import shutil


def baue_pfad(X1_map, X2_map, X3_map, X4_map, X5_map, X6_map, sTargetFolder):
    try:
        pfadteile = [X1_map, X2_map, X3_map, X4_map, X5_map, X6_map]
        sTargetFolderJoint = os.path.join(sTargetFolder, *pfadteile)
        return sTargetFolderJoint
    except TypeError:
        print("Fehler: Eine der Listen enthält unerwartete Daten.")
        return None


def verschiebe_datei(sSortFile, sSourceFolder, sTargetFolderJoint):
    try:
        source_path = os.path.join(sSourceFolder, sSortFile)
        target_path = os.path.join(sTargetFolderJoint, sSortFile)

        if not os.path.exists(sTargetFolderJoint):
            os.makedirs(sTargetFolderJoint)

        shutil.move(source_path, target_path)
        print(f"Die Datei {sSortFile} wurde erfolgreich verschoben.")
    except FileNotFoundError:
        print(f"Fehler: Die Datei {sSortFile} wurde im Quellordner nicht gefunden.")
    except PermissionError:
        print(f"Fehler: Keine Berechtigung, um die Datei {sSortFile} zu verschieben.")
    except Exception as e:
        print(
            f"Ein unerwarteter Fehler ist aufgetreten beim Verschieben von {sSortFile}: {e}"
        )


def finde_listen_mit_inhalt(**kwargs):
    lToSort = []
    for name, liste in kwargs.items():
        if liste:
            lToSort.append(name)
    return lToSort


def aktualisiere_map_listen(**kwargs):
    result = {}
    for name, value in kwargs.items():
        if name.endswith("_map"):
            xn_name = name[:-4]
            if xn_name in kwargs and not value:
                result[name] = kwargs[xn_name]
            else:
                result[name] = value
        else:
            result[name] = value
    return result


def suche_dateien(sSourceFolder, **kwargs):
    try:
        gefundene_dateien = []
        gefuellte_listen = finde_listen_mit_inhalt(**kwargs)

        for datei in os.listdir(sSourceFolder):
            # Überprüfen, ob alle Bedingungen aller gefüllten Listen erfüllt sind
            if all(
                any(wert in datei for wert in kwargs[liste_name])
                for liste_name in gefuellte_listen
            ):
                gefundene_dateien.append(datei)

        return gefundene_dateien
    except Exception as e:
        print(f"Ein Fehler ist beim Durchsuchen des Ordners aufgetreten: {e}")
        return


def sorting_agent(sTargetFolder, sSourceFolder, **kwargs):
    try:
        aktualisierte_listen = aktualisiere_map_listen(**kwargs)

        sTargetFolderJoint = baue_pfad(
            aktualisierte_listen["X1_map"],
            aktualisierte_listen["X2_map"],
            aktualisierte_listen["X3_map"],
            aktualisierte_listen["X4_map"],
            aktualisierte_listen["X5_map"],
            aktualisierte_listen["X6_map"],
            sTargetFolder,
        )
        if sTargetFolderJoint is None:
            return

        # Dateien, die gefunden wurden
        zu_verschiebende_dateien = suche_dateien(sSourceFolder, **kwargs)

        # Verschiebe die gefundenen Dateien
        for datei in zu_verschiebende_dateien:
            verschiebe_datei(datei, sSourceFolder, sTargetFolderJoint)

        # Alle Dateien im Quellordner
        alle_dateien = os.listdir(sSourceFolder)

        # Dateien, die nicht gefunden wurden
        nicht_gefundene_dateien = [
            datei for datei in alle_dateien if datei not in zu_verschiebende_dateien
        ]

        # Zielordner für nicht gefundene Dateien
        sNotFoundFolder = os.path.join(sTargetFolder, "notfound")

        # Verschiebe nicht gefundene Dateien
        for datei in nicht_gefundene_dateien:
            verschiebe_datei(datei, sSourceFolder, sNotFoundFolder)

    except Exception as e:
        print(f"Ein Hauptfehler ist im sorting_agent aufgetreten: {e}")
