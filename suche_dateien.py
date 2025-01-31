import os


def suche_dateien(sSourceFolder, **kwargs):
    """
    Durchsucht den sSourceFolder nach Dateien, die Kombinationen aus den gefüllten Listen enthalten.

    :param sSourceFolder: Der Pfad zum zu durchsuchenden Ordner
    :param kwargs: Keyword-Argumente, die Listen für die Suche enthalten
    :return: Liste der Dateien, die die gesuchten Kombinationen enthalten
    """
    gefundene_dateien = []
    gefuellte_listen = finde_listen_mit_inhalt(**kwargs)

    # Generiere alle möglichen Kombinationen
    import itertools

    kombinationen = []
    listen = [kwargs[liste_name] for liste_name in gefuellte_listen]
    for lengths in itertools.product(*(range(1, len(liste) + 1) for liste in listen)):
        for combo in itertools.product(
            *[liste[:length] for liste, length in zip(listen, lengths)]
        ):
            kombinationen.append(combo)

    # Durchsuche Dateinamen
    for datei in os.listdir(sSourceFolder):
        if any(all(wert in datei for wert in kombi) for kombi in kombinationen):
            gefundene_dateien.append(datei)

    return gefundene_dateien
