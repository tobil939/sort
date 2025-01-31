def aktualisiere_map_listen(**kwargs):
    """
    Aktualisiert die Xn_map-Listen, indem es Werte aus den entsprechenden Xn-Listen übernimmt, wenn Xn_map leer ist.

    :param kwargs: Keyword-Argumente, wobei die Schlüssel die Namen der Listen sind und die Werte die Listen selbst
    :return: Ein Dictionary mit aktualisierten Xn_map-Listen
    """
    result = {}

    # Iteriere durch alle übergebenen Listen
    for name, value in kwargs.items():
        if name.endswith("_map"):
            # Finde den Namen der entsprechenden X-Liste durch Entfernen von '_map'
            xn_name = name[:-4]
            if xn_name in kwargs and not value:  # Wenn die Xn_map-Liste leer ist
                result[name] = kwargs[xn_name]  # Übernehme Werte von Xn
            else:
                result[name] = value  # Andernfalls behalte die Xn_map-Liste bei
        else:
            # Speichere die X-Listen einfach durch, da sie keine '_map' sind
            result[name] = value

    return result


# Beispielaufruf der Funktion:
# Angenommen, wir haben:
# X1 = ["-20Deg", "23Deg", "50Deg"]
# X1_map = ["LT", "RT", "HT"]
# X5 = ["20Nm", "30Nm"]
# X5_map = []

# result = aktualisiere_map_listen(X1=X1, X1_map=X1_map, X5=X5, X5_map=X5_map)
# print(result)  # Würde {'X1': ['-20Deg', '23Deg', '50Deg'], 'X1_map': ['LT', 'RT', 'HT'],
#                #        'X5': ['20Nm', '30Nm'], 'X5_map': ['20Nm', '30Nm']} ausgeben
