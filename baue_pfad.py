import os


def baue_pfad(X1_map, X2_map, X3_map, X4_map, X5_map, X6_map, sTargetFolder):
    """
    Baut einen Pfad aus den gegebenen Listenwerten und einem Basisordner.

    :param X1_map - X6_map: Listen mit Werten, die in den Pfad eingebaut werden
    :param sTargetFolder: Basisordner, in dem der neue Pfad erstellt wird
    :return: Der zusammengesetzte Pfad als String
    """
    try:
        # Kombiniere die Werte aus den Listen zu einem Pfad
        pfadteile = [X1_map, X2_map, X3_map, X4_map, X5_map, X6_map]

        # Füge alle Teile zusammen, um den vollständigen Pfad zu bilden
        sTargetFolderJoint = os.path.join(sTargetFolder, *pfadteile)

        return sTargetFolderJoint
    except TypeError as e:
        print(f"Fehler: Es wurde ein unerwarteter Datentyp übergeben. {e}")
    except Exception as e:
        print(f"Ein unvorhergesehener Fehler ist aufgetreten: {e}")
    return None  # Gibt None zurück, wenn ein Fehler auftritt


# Beispielaufruf der Funktion:
# Beispielwerte:
# X1_map = "Wert1"
# X2_map = "Wert2"
# X3_map = "Wert3"
# X4_map = "Wert4"
# X5_map = "Wert5"
# X6_map = "Wert6"
# sTargetFolder = "/Pfad/Zum/BasisOrdner"

# sTargetFolderJoint = baue_pfad(X1_map, X2_map, X3_map, X4_map, X5_map, X6_map, sTargetFolder)
# print(sTargetFolderJoint)
