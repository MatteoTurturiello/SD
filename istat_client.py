import csv
import io
import xml.etree.ElementTree as ET
import requests

ISTAT_INCIDENTS_URL = (
    "https://esploradati.istat.it/SDMXWS/rest/data/"
    "41_983/A.048017.ROADACC.9"
)
ISTAT_POPULATION_URL = (
    "https://esploradati.istat.it/SDMXWS/rest/data/"
    "IT1,22_289/A.048017.JAN.9.TOTAL.99/"
)
TIMEOUT = (10, 150)


def _check_response(response):
    response.raise_for_status()
    if not response.text.strip():
        raise ValueError("ISTAT ha restituito una risposta vuota.")
    return response


def get_incidents_by_year():
    """Restituisce {anno: incidenti} per tutti gli anni restituiti da ISTAT."""
    response = requests.get(ISTAT_INCIDENTS_URL, timeout=TIMEOUT)
    _check_response(response)
    root = ET.fromstring(response.content)
    values = {}

    for obs in root.iter():
        if not obs.tag.endswith("Obs"):
            continue
        year = value = None
        for element in obs:
            if element.tag.endswith("ObsDimension"):
                year = element.attrib.get("value")
            elif element.tag.endswith("ObsValue"):
                value = element.attrib.get("value")
        if year and value is not None:
            try:
                values[str(year)] = int(float(value))
            except (TypeError, ValueError):
                pass

    if not values:
        raise ValueError(
            "Nessun dato sugli incidenti trovato nella risposta ISTAT. "
            "Verifica che la risposta contenga osservazioni e non una risposta di test."
        )
    return values


def get_population_by_year():
    """Restituisce {anno: popolazione} dal CSV ISTAT."""
    response = requests.get(
        ISTAT_POPULATION_URL,
        headers={"Accept": "text/csv"},
        timeout=TIMEOUT,
    )
    _check_response(response)
    reader = csv.DictReader(io.StringIO(response.text))
    values = {}

    for row in reader:
        year = row.get("TIME_PERIOD")
        value = row.get("OBS_VALUE")
        if not year or value in (None, ""):
            continue
        try:
            values[str(year)] = int(float(value))
        except (TypeError, ValueError):
            pass

    if not values:
        raise ValueError(
            "Nessun dato sulla popolazione trovato. "
            "Verifica che ISTAT restituisca il CSV atteso."
        )
    return values


def _build_p6(year, incidents, population):
    year = str(year)
    if year not in incidents:
        raise ValueError(f"Incidenti ISTAT non disponibili per l'anno {year}.")
    if year not in population:
        raise ValueError(f"Popolazione ISTAT non disponibile per l'anno {year}.")
    n_incidents = incidents[year]
    n_inhabitants = population[year]
    if n_inhabitants <= 0:
        raise ValueError(f"Popolazione non valida per l'anno {year}.")

    return {
        "municipality": "Firenze",
        "referenceYear": int(year),
        "indicator": "P6 - Incidentality",
        "roadAccidents": n_incidents,
        "nInhabitants": n_inhabitants,
        "multiplier": 10000,
        "indicatorValue": round((n_incidents / n_inhabitants) * 10000, 2),
        "dateObserved": f"{year}-01-01T00:00:00Z",
    }


def get_p6_for_year(year):
    """Calcola P6 per un singolo anno."""
    incidents = get_incidents_by_year()
    population = get_population_by_year()
    return _build_p6(year, incidents, population)


def get_all_p6_years():
    """Restituisce gli anni comuni ai dataset incidenti e popolazione."""
    incidents = get_incidents_by_year()
    population = get_population_by_year()
    common_years = sorted(set(incidents) & set(population), key=int)

    if not common_years:
        raise ValueError(
            "Nessun anno comune tra i dataset ISTAT di incidenti e popolazione."
        )

    results = []
    for year in common_years:
        if population[year] > 0:
            results.append(_build_p6(year, incidents, population))
    if not results:
        raise ValueError("Non è stato possibile calcolare alcun valore P6.")
    return results
