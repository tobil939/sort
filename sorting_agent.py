import os
import shutil


def baue_pfad(X1_map, X2_map, X3_map, X4_map, X5_map, X6_map, sTargetFolder):
    """
    Baut einen Pfad aus den gegebenen Listenwerten und einem Basisordner.

    :param X1_map - X6_map: Listen mit Werten, die in den Pfad eingebaut werden
    :param sTargetFolder: Basisordner, in dem der neue Pfad erstellt wird
    :return: Der zusammengesetzte Pfad als String
    """
    try:
        pfadteile = [X1_map, X2_map, X3_map, X4_map, X5_map, X6_map]
        sTargetFolderJoint = os.path.join(sTargetFolder, *pfadteile)
        return sTargetFolderJoint
    except TypeError:
        print("Fehler: Eine der Listen enthält unerwartete Daten.")
        return None


def verschiebe_datei(sSortFile, sSourceFolder, sTargetFolderJoint):
    """
    Verschiebt eine Datei von einem Quellordner in einen Zielordner.
    Falls der Zielordner nicht existiert, wird er erstellt.

    :param sSortFile: Name der zu verschiebenden Datei
    :param sSourceFolder: Quellordner der Datei
    :param sTargetFolderJoint: Zielordner der Datei
    """
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
    """
    Überprüft, ob die übergebenen Listen Inhalte haben und speichert die Namen der nicht-leeren Listen.

    :param kwargs: Keyword-Argumente, wobei die Schlüssel die Namen der Listen sind und die Werte die Listen selbst
    :return: Eine Liste mit den Namen der Listen, die Inhalte enthalten
    """
    lToSort = []
    for name, liste in kwargs.items():
        if liste:
            lToSort.append(name)
    return lToSort


def aktualisiere_map_listen(**kwargs):
    """
    Aktualisiert die Xn_map-Listen, indem es Werte aus den entsprechenden Xn-Listen übernimmt, wenn Xn_map leer ist.

    :param kwargs: Keyword-Argumente, wobei die Schlüssel die Namen der Listen sind und die Werte die Listen selbst
    :return: Ein Dictionary mit aktualisierten Xn_map-Listen
    """
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
    """
    Durchsucht den sSourceFolder nach Dateien, die Kombinationen aus den gefüllten Listen enthalten.

    :param sSourceFolder: Der Pfad zum zu durchsuchenden Ordner
    :param kwargs: Keyword-Argumente, die Listen für die Suche enthalten
    :return: Liste der Dateien, die die gesuchten Kombinationen enthalten
    """
    try:
        gefundene_dateien = []
        gefuellte_listen = finde_listen_mit_inhalt(**kwargs)

        import itertools

        kombinationen = []
        listen = [kwargs[liste_name] for liste_name in gefuellte_listen]
        for lengths in itertools.product(
            *(range(1, len(liste) + 1) for liste in listen)
        ):
            for combo in itertools.product(
                *[liste[:length] for liste, length in zip(listen, lengths)]
            ):
                kombinationen.append(combo)

        for datei in os.listdir(sSourceFolder):
            if any(all(wert in datei for wert in kombi) for kombi in kombinationen):
                gefundene_dateien.append(datei)

        return gefundene_dateien
    except Exception as e:
        print(f"Ein Fehler ist beim Durchsuchen des Ordners aufgetreten: {e}")
        return []


def sorting_agent(sTargetFolder, sSourceFolder, **kwargs):
    """
    Hauptprogramm, das Dateien aus sSourceFolder basierend auf den Inhalten von Xn in sTargetFolderJoint sortiert.

    :param sTargetFolder: Der Basisordner für das Ziel
    :param sSourceFolder: Der Quellordner
    :param kwargs: Keyword-Argumente für Xn und Xn_map Listen
    """
    try:
        # Aktualisiere die Xn_map Listen
        aktualisierte_listen = aktualisiere_map_listen(**kwargs)

        # Baue den Zielpfad
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

        # Suche nach Dateien
        zu_verschiebende_dateien = suche_dateien(sSourceFolder, **kwargs)

        # Verschiebe die gefundenen Dateien
        for datei in zu_verschiebende_dateien:
            verschiebe_datei(datei, sSourceFolder, sTargetFolderJoint)

    except Exception as e:
        print(f"Ein Hauptfehler ist im sorting_agent aufgetreten: {e}")


# Beispielaufruf:
# sTargetFolder = "/Pfad/Zum/Zielordner"
# sSourceFolder = "/Pfad/Zum/Quellordner"
# X1 = ["-20Deg", "23Deg"]
# X1_map = ["LT", "RT"]
# X4 = ["20Nm"]
# X4_map = []
# X5 = ["Test"]
# X5_map = []
# X2 = []; X3 = []; X6 = []; X2_map = []; X3_map = []; X6_map = []

# sorting_agent(sTargetFolder, sSourceFolder, X1=X1, X1_map=X1_map, X2=X2, X2_map=X2_map,
#               X3=X3, X3_map=X3_map, X4=X4, X4_map=X4_map, X5=X5, X5_map=X5_map,
#               X6=X6, X6_map=X6_map)

