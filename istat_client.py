import csv
import io
import requests
import xml.etree.ElementTree as ET
URL_ISTAT_POPOLAZIONE = (
    "https://esploradati.istat.it/SDMXWS/rest/v2/"
    "data/dataflow/IT1/22_389/1.0/"
    "A.048017.JAN.9.TOTAL.99"
)



def get_population_by_year(year=None):
    url = (
        "https://esploradati.istat.it/SDMXWS/rest/data/"
        "IT1,22_289/A.048017.JAN.9.TOTAL.99/"
    )

    headers = {"Accept": "text/csv"}

    response = requests.get(
        url,
        headers=headers,
        timeout=(10, 150)
    )
    response.raise_for_status()

    righe = csv.DictReader(io.StringIO(response.text))
    popolazione_per_anno = {}

    for riga in righe:
        anno = riga.get("TIME_PERIOD")
        valore = riga.get("OBS_VALUE")

        if anno and valore:
            popolazione_per_anno[anno] = int(float(valore))

    if not popolazione_per_anno:
        raise ValueError(
            "Nessun dato sulla popolazione trovato nella risposta ISTAT."
        )

    if year is None:
        anno_scelto = max(popolazione_per_anno, key=int)
    else:
        anno_scelto = str(year)

        if not anno_scelto.isdigit():
            raise ValueError(
                "L'anno deve essere un numero, ad esempio 2024."
            )

        if anno_scelto not in popolazione_per_anno:
            anni = sorted(popolazione_per_anno, key=int)
            raise ValueError(
                f"Popolazione per l'anno {anno_scelto} non disponibile. "
                f"Anni restituiti da ISTAT: {anni[0]}-{anni[-1]}."
            )

    return {
        "municipality": "Firenze",
        "referenceYear": int(anno_scelto),
        "nInhabitants": popolazione_per_anno[anno_scelto]
    }


URL_ISTAT = (
    "https://esploradati.istat.it/SDMXWS/rest/data/"
    "41_983/A.048017.ROADACC.9"
)


def get_incidents_by_year():
    """
    Recupera da ISTAT gli incidenti stradali con lesioni
    alle persone per il Comune di Firenze.

    Restituisce un dizionario:
    {anno: numero_incidenti}
    """

    response = requests.get(URL_ISTAT, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    incidenti_per_anno = {}

    for obs in root.iter():
        if obs.tag.endswith("Obs"):
            anno = None
            valore = None

            for elemento in obs:
                if elemento.tag.endswith("ObsDimension"):
                    anno = elemento.attrib.get("value")

                elif elemento.tag.endswith("ObsValue"):
                    valore = elemento.attrib.get("value")

            if anno is not None and valore is not None:
                incidenti_per_anno[anno] = int(valore)

    if not incidenti_per_anno:
        raise ValueError(
            "Nessuna osservazione trovata nella risposta ISTAT."
        )

    return incidenti_per_anno


def get_incidents_for_year(year=None):
    """
    Restituisce il numero di incidenti per un anno specifico.

    Se year è None, seleziona l'ultimo anno presente
    nei dati restituiti da ISTAT.
    """

    incidenti_per_anno = get_incidents_by_year()

    if year is None:
        anno_scelto = max(incidenti_per_anno, key=int)
    else:
        anno_scelto = str(year)

        if not anno_scelto.isdigit():
            raise ValueError(
                "L'anno deve essere un numero, ad esempio 2024."
            )

        if anno_scelto not in incidenti_per_anno:
            anni = sorted(incidenti_per_anno, key=int)

            raise ValueError(
                f"Anno {anno_scelto} non disponibile. "
                f"Anni presenti: {anni[0]}-{anni[-1]}."
            )

    return {
        "municipality": "Firenze",
        "referenceYear": int(anno_scelto),
        "roadAccidents": incidenti_per_anno[anno_scelto]
    }
