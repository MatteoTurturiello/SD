def calculate_p6(road_accidents, n_inhabitants, multiplier=10000):
    """Calcola gli incidenti stradali ogni multiplier abitanti."""
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
    return (road_accidents / n_inhabitants) * multiplier
