def finde_listen_mit_inhalt(**kwargs):
    """
    Überprüft, ob die übergebenen Listen Inhalte haben und speichert die Namen der nicht-leeren Listen.

    :param kwargs: Keyword-Argumente, wobei die Schlüssel die Namen der Listen sind und die Werte die Listen selbst
    :return: Eine Liste mit den Namen der Listen, die Inhalte enthalten
    """
    lToSort = []

    for name, liste in kwargs.items():
        if liste:  # Überprüft, ob die Liste nicht leer ist
            lToSort.append(name)

    return lToSort
