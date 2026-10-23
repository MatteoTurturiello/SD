
from fastapi import FastAPI, HTTPException
from requests.exceptions import RequestException

from istat_client import (
    get_incidents_for_year,
    get_population_by_year
)
from p6_calculator import calculate_p6

app = FastAPI(
    title="PUMS API",
    description="API per il calcolo degli indicatori PUMS",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "API PUMS attiva",
        "indicatori": ["P6 - Incidentality"]
    }


@app.get("/api/pums/p6/{year}")
def get_p6(year: int):
    try:
        incidenti = get_incidents_for_year(year)
        popolazione = get_population_by_year(year)

        indice = calculate_p6(
            incidenti["roadAccidents"],
            popolazione["nInhabitants"],
            multiplier=10000
        )

        return {
            "municipality": "Firenze",
            "referenceYear": year,
            "indicator": "P6 - Incidentality",
            "roadAccidents": incidenti["roadAccidents"],
            "nInhabitants": popolazione["nInhabitants"],
            "multiplier": 10000,
            "indicatorIncidentality": round(indice, 2)
        }

    except (ValueError, RequestException) as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
