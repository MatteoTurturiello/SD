
def calculate_p6(road_accidents, n_inhabitants, multiplier=10000):
    """
    Calcola l'indicatore P6 - Incidentalità stradale.

    Formula:
        P6 = (incidenti / popolazione) * multiplier

    Parametri:
        road_accidents: numero di incidenti con lesioni
        n_inhabitants: popolazione residente
        multiplier: fattore di scala, ad esempio 10000

    Restituisce:
        Valore numerico dell'indicatore P6
    """

    if not isinstance(road_accidents, int) or isinstance(road_accidents, bool):
        raise ValueError("Il numero di incidenti deve essere un intero.")

    if road_accidents < 0:
        raise ValueError("Il numero di incidenti non può essere negativo.")

    if not isinstance(n_inhabitants, int) or isinstance(n_inhabitants, bool):
        raise ValueError("La popolazione deve essere un numero intero.")

    if n_inhabitants <= 0:
        raise ValueError("La popolazione deve essere maggiore di zero.")

    if not isinstance(multiplier, int) or isinstance(multiplier, bool):
        raise ValueError("Il moltiplicatore deve essere un intero.")

    if multiplier <= 0:
        raise ValueError("Il moltiplicatore deve essere maggiore di zero.")

    p6 = (road_accidents / n_inhabitants) * multiplier

    return p6
