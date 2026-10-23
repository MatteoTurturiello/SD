from fastapi import FastAPI, HTTPException
from requests.exceptions import RequestException
from istat_client import get_all_p6_years, get_p6_for_year

app = FastAPI(
    title="PUMS API",
    description="API per il calcolo degli indicatori PUMS",
    version="1.1.0",
)


@app.get("/")
def home():
    return {
        "message": "API PUMS attiva",
        "indicatori": ["P6 - Incidentalità"],
        "endpoints": ["/api/pums/p6/{year}", "/api/pums/p6"],
    }


@app.get("/api/pums/p6")
def get_all_p6():
    """Restituisce tutti gli anni con dati disponibili in entrambe le fonti ISTAT."""
    try:
        years = get_all_p6_years()
        return {
            "municipality": "Firenze",
            "indicator": "P6 - Incidentality",
            "count": len(years),
            "years": years,
        }
    except (ValueError, RequestException) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/pums/p6/{year}")
def get_p6(year: int):
    """Restituisce il valore P6 di un singolo anno."""
    try:
        return get_p6_for_year(year)
    except (ValueError, RequestException) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
